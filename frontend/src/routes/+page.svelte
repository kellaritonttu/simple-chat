<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { auth, signInWithGoogle, logout } from '$lib/firebase';
  import { onAuthStateChanged } from 'firebase/auth';

  interface Message {
    id: number;
    text: string;
    user_id: string;
    display_name: string;
    created_at: string;
    edited_at: string | null;
  }

  let messages = $state<Message[]>([]);
  let input = $state('');
  let interval: ReturnType<typeof setInterval>;

  let currentUserId = $state<string | null>(null);
  let currentUser = $state<any>(null);
  let token = $state<string | null>(null);
  let displayName = $state('');
  let newDisplayName = $state('');
  let showAccount = $state(false);

  // State to track editing
  let editingId = $state<number | null>(null);
  let editText = $state('');

  const API = '/api';

  async function getHeaders(): Promise<HeadersInit> {
    if (currentUser) {
      token = await currentUser.getIdToken(); // refreshes if expired
    }
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };
  }

  async function loadMessages() {
    const res = await fetch('/api/messages/', {
      headers: await getHeaders()
    });
    messages = await res.json();
  }

  async function sendMessage() {
      if (!input.trim()) return;
    
      const res = await fetch('/api/messages/', {
        method: 'POST',
        headers: await getHeaders(),
        body: JSON.stringify({ text: input }),
      });
    
      input = '';
  }

  function startEdit(message: Message) {
    editingId = message.id;
    editText  = message.text;
  }

  function cancelEdit() {
    editingId = null;
    editText = '';
  }

  async function saveEdit(id: number) {
    if (!editText.trim()) return;

    const res = await fetch(`${API}/messages/${id}`, {
      method: 'PATCH',
      headers: await getHeaders(),
      body: JSON.stringify({ text: editText }),
    });

    if (res.ok) {
      const updated = await res.json();
      messages = messages.map((m) => (m.id === id ? updated : m));
      cancelEdit();
    }
  }

  async function deleteMessage(id: number) {
    const res = await fetch(`${API}/messages/${id}`, {
      method: 'DELETE',
      headers: await getHeaders(),
    });

    if (res.ok) {
      messages = messages.filter((m) => m.id !== id);
    }
  }

  async function updateDisplayName() {
    if (!newDisplayName.trim()) return;

    const res = await fetch('/api/users/me', {
      method: 'PATCH',
      headers: await getHeaders(),
      body: JSON.stringify({ display_name: newDisplayName }),
    });

    if (res.ok) {
      // don't touch currentUser here — it must stay the real Firebase User
      // object so getIdToken() keeps working. Track the shown name separately.
      displayName = newDisplayName;
      newDisplayName = '';
      showAccount = false;
    }
  }

  async function deleteAccount() {
    if (!confirm('Delete your account and all messages?')) return;
    
    await fetch('/api/users/me', {
      method: 'DELETE',
      headers: await getHeaders(),
    });
    
    await logout();
  }

  onMount(() => {
    const unsub = onAuthStateChanged(auth, async (user) => {
      currentUser = user;
      if (user) {
        token = await user.getIdToken();
        displayName = user.displayName || user.email || '';

        // register in backend on first login — idempotent
        await fetch('/api/users/', {
          method: 'POST',
          headers: await getHeaders(),
          body: JSON.stringify({
            id: user.uid,
            display_name: displayName
          }),
        });

        loadMessages();
        interval = setInterval(loadMessages, 3000);
      } else {
        clearInterval(interval);
        messages = [];
      }
    });

    return () => {
      unsub();
      clearInterval(interval);
    };
  });
</script>


<main>
  {#if !currentUser}
    <!-- Login page -->
    <div class="flex justify-center items-center h-screen">
      <div class="text-center">
        <h1 class="text-3xl font-bold mb-8">Chat</h1>
        <button
          class="bg-white border rounded px-6 py-3 flex items-center gap-3 shadow hover:shadow-md"
          onclick={signInWithGoogle}
        >
          Sign in with Google
        </button>
      </div>
    </div>

  {:else}
    <!-- Chat + account panel -->
    <div class="max-w-xl mx-auto p-4">

      <!-- Account bar -->
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold">Chat</h1>
        <div class="flex items-center gap-3">
          <span class="text-sm text-gray-600">{displayName}</span>
          <button onclick={() => showAccount = !showAccount} class="text-sm text-blue-500">
            Account
          </button>
          <button onclick={logout} class="text-sm text-red-500">
            Sign out
          </button>
        </div>
      </div>

      <!-- Account panel -->
      {#if showAccount}
        <div class="bg-white border rounded p-4 mb-4">
          <h2 class="font-semibold mb-3">Account settings</h2>
          <div class="flex gap-2">
            <input
              class="flex-1 border rounded p-2 text-sm"
              bind:value={newDisplayName}
              placeholder="New display name"
            />
            <button
              class="bg-blue-500 text-white px-3 py-1 rounded text-sm"
              onclick={updateDisplayName}
            >
              Update
            </button>
          </div>
          <button
            class="text-red-500 text-sm mt-3"
            onclick={deleteAccount}
          >
            Delete account
          </button>
        </div>
      {/if}

      <div class="flex flex-col gap-2 mb-4">
        {#each messages as message (message.id)}
          <div class="border rounded p-2">
            {#if editingId === message.id}
              <div class="flex gap-2">
                <input
                  class="flex-1 border rounded p-1 text-sm"
                  bind:value={editText}
                  onkeydown={(e) => e.key === 'Enter' && saveEdit(message.id)}
                />
                <button class="text-sm text-blue-500" onclick={() => saveEdit(message.id)}>Save</button>
                <button class="text-sm text-gray-500" onclick={cancelEdit}>Cancel</button>
              </div>
            {:else}
              <div class="flex justify-between items-start gap-2">
                <div>
                  <strong>{message.display_name}</strong>: {message.text}
                  {#if message.edited_at}
                    <span class="text-xs text-gray-400">(edited)</span>
                  {/if}
                </div>
                {#if message.user_id === currentUser?.uid}
                  <div class="flex gap-2 shrink-0">
                    <button class="text-xs text-blue-500" onclick={() => startEdit(message)}>Edit</button>
                    <button class="text-xs text-red-500" onclick={() => deleteMessage(message.id)}>Delete</button>
                  </div>
                {/if}
              </div>
            {/if}
          </div>
        {/each}
      </div>

      <div class="flex gap-2">
        <input
          class="flex-1 border rounded p-2"
          bind:value={input}
          placeholder="Type a message..."
          onkeydown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button
          class="bg-blue-500 text-white px-4 py-2 rounded"
          onclick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  {/if}
</main>