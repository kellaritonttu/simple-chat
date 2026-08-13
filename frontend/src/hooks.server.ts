import type { Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

export const handle: Handle = async ({ event, resolve }) => {
  const backendUrl = env.BACKEND_URL;

  // 1. Proxy /api/* to backend — STRIP /api/ prefix like nginx did
  if (event.url.pathname.startsWith('/api/')) {
    if (!backendUrl) {
      return new Response('BACKEND_URL not configured', { status: 500 });
    }

    const backendPath = event.url.pathname.replace(/^\/api/, '');
    const target = backendUrl.replace(/\/$/, '') + backendPath + event.url.search;

    const response = await fetch(target, {
      method: event.request.method,
      headers: event.request.headers,
      body: event.request.body,
      // @ts-ignore
      duplex: 'half'
    });

    return response;
  }

  // 2. Normal SvelteKit rendering
  const response = await resolve(event);

  // 3. COOP header for Firebase popup auth
  response.headers.set('Cross-Origin-Opener-Policy', 'same-origin-allow-popups');

  // 4. Never cache index.html
  if (event.url.pathname === '/') {
    response.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
    response.headers.set('Pragma', 'no-cache');
  }

  return response;
};