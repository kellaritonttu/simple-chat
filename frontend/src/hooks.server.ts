import type { Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

export const handle: Handle = async ({ event, resolve }) => {
  if (event.url.pathname.startsWith('/api')) {
    const backendUrl = env.BACKEND_URL;
    if (!backendUrl) {
      return new Response('BACKEND_URL not configured', { status: 500 });
    }

    const backendPath = event.url.pathname.replace(/^\/api\/?/, '');
    const target = backendUrl.replace(/\/$/, '') + '/' + backendPath + event.url.search;
    console.log(`Proxying ${event.url.pathname} -> ${target}`);

    // Strip hop-by-hop headers
    const headers = new Headers(event.request.headers);
    headers.delete('host');
    headers.delete('connection');

    const upstream = await fetch(target, {
      method: event.request.method,
      headers,
      body: event.request.body,
      // @ts-ignore
      duplex: 'half'
    });

    const responseHeaders = new Headers(upstream.headers);
    responseHeaders.delete('content-encoding');
    responseHeaders.delete('content-length');

    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: responseHeaders
    });
  }

  const response = await resolve(event);
  response.headers.set('Cross-Origin-Opener-Policy', 'same-origin-allow-popups');
  if (event.url.pathname === '/') {
    response.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
    response.headers.set('Pragma', 'no-cache');
  }
  return response;
};