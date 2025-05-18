const pathToRegexp = require('path-to-regexp');
const routes = require('./routes');

function compileRoutes(routes) {
  return routes.map(route => {
    try {
      const keys = [];
      const re = pathToRegexp(route.path, keys);
      return {
        ...route,
        regexp: re,
        keys: keys,
      };
    } catch (error) {
      console.error(`Error compiling route ${route.path}:`, error);
      return null; // Or handle the error as appropriate for your application
    }
  }).filter(Boolean);
}

const compiledRoutes = compileRoutes(routes);

console.log('Compiled Routes:', compiledRoutes);

// Example usage (replace with your actual request handling logic)
function handleRequest(url) {
  for (const route of compiledRoutes) {
    const match = route.regexp.exec(url);
    if (match) {
      console.log(`Matched route: ${route.path}`);
      // Extract parameters from the match and keys
      const params = {};
      route.keys.forEach((key, i) => {
        params[key.name] = match[i + 1];
      });
      console.log('Parameters:', params);
      return; // Stop after the first match
    }
  }
  console.log('No route matched.');
}

// Example requests
handleRequest('/products/123');
handleRequest('/categories/456');
handleRequest('/about');
handleRequest('/search');
handleRequest('/invalid/:'); //This will not match any route, as it is invalid