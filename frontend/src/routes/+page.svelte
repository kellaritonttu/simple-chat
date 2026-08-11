<script lang="ts">
  import { onMount } from 'svelte';

  interface Message {
    id: number;
    text: string;
    created_at: string;
    edited_at: string;
  }

  let messages = $state<Message[]>([]);
  let input = $state('');

  // State to track editing
  let editingId = $state<number | null>(null);
  let editText = $state('');

  const API = '/api';

  async function loadMessages() {
    const res = await fetch(`${API}/messages/`);
    messages = await res.json();
  }

  async function sendMessage() {
    if (!input.trim()) return;

    const res = await fetch(`${API}/messages/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input }),
    });

    const message = await res.json();
    messages = [...messages, message];
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
      headers: { 'Content-Type': 'application/json' },
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
    });

    if (res.ok) {
      messages = messages.filter((m) => m.id !== id);
    }
  }

  onMount(loadMessages);
</script>


<main class="max-w-xl mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Chat</h1>

  <div class="flex flex-col gap-2 mb-4">
    {#each messages as message (message.id)}
      <div class="bg-gray-100 rounded p-3 flex flex-col gap-2">
        {#if editingId === message.id}
          <!-- Edit Mode -->
          <div class="flex gap-2">
            <input
              class="flex-1 border rounded p-2 text-sm bg-white"
              bind:value={editText}
              onkeydown={(e) => e.key === 'Enter' && saveEdit(message.id)}
            />
            <button
              class="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
              onclick={() => saveEdit(message.id)}
            >
              Save
            </button>
            <button
              class="bg-gray-300 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-400"
              onclick={cancelEdit}
            >
              Cancel
            </button>
          </div>
        {:else}
          <!-- Normal Mode -->
          <div class="flex justify-between items-start">
            <div>
              <p>{message.text}</p>
              <span class="text-xs text-gray-400">
                {new Date(message.edited_at || message.created_at).toLocaleTimeString()}
              </span>
              {#if message.edited_at}
                <span class="text-xs text-blue-500">(edited)</span>
              {/if}
            </div>

            <div class="flex gap-2">
              <button
                class="text-xs text-blue-600 hover:underline"
                onclick={() => startEdit(message)}
              >
                Edit
              </button>
              <button
                class="text-xs text-red-600 hover:underline"
                onclick={() => deleteMessage(message.id)}
              >
                Delete
              </button>
            </div>
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
</main>