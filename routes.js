const routes = [
  {
    path: '/products/:productId', // Correct: Parameter name 'productId' is present
    handler: 'handleProducts',
  },
  {
    path: '/categories/:categoryId', // Corrected: Added parameter name 'categoryId'
    handler: 'handleCategories',
  },
  {
    path: '/about', // Correct: No parameters
    handler: 'handleAbout',
  },
  {
    path: '/search',
    handler: 'handleSearch',
  },
];

module.exports = routes;