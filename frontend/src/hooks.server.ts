import type { Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';


export const handle: Handle = async ({ event, resolve }) => {
  if (event.platform && 'prerender' in event.platform && event.platform.prerender) {
    return await resolve(event);
  }

  const backendUrl = env.BACKEND_URL;
  if (!backendUrl) {
    console.error('BACKEND_URL is missing!');
    return new Response('BACKEND_URL not configured', { status: 500 });
  }

  // Proxy /api/* to backend
  if (event.url.pathname.startsWith('/api')) {
    const backendPath = event.url.pathname.replace(/^\/api\/?/, '');
    const target = backendUrl.replace(/\/$/, '') + '/' + backendPath + event.url.search;

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