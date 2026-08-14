import type { Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

export const handle: Handle = async ({ event, resolve }) => {
  const backendUrl = env.BACKEND_URL;
  if (!backendUrl) {
    return new Response('BACKEND_URL not configured', { status: 500 });
  }

  // Match ALL `/api*` paths (with or without trailing slashes)
  if (event.url.pathname.startsWith('/api')) {
    // Strip `/api` and any following slash (e.g., `/api` → ``, `/api/` → ``, `/api/foo` → `/foo`)
    const backendPath = event.url.pathname.replace(/^\/api\/?/, '');
    const target = backendUrl.replace(/\/$/, '') + '/' + backendPath + event.url.search;

    console.log(`Proxying ${event.url.pathname} → ${target}`); // Debug log

    const response = await fetch(target, {
      method: event.request.method,
      headers: event.request.headers,
      body: event.request.body,
    // @ts-ignore
      duplex: 'half'
    });
    return response;
  }

  // Normal SvelteKit rendering
  const response = await resolve(event);
  response.headers.set('Cross-Origin-Opener-Policy', 'same-origin-allow-popups');
  if (event.url.pathname === '/') {
    response.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
    response.headers.set('Pragma', 'no-cache');
  }
  return response;
};