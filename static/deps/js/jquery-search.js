const searchForm = document.querySelector('.d-flex[role="search"]');
searchForm.addEventListener('submit', (event) => {
  const searchQuery = document.querySelector('input[name="q"]').value;

  if (searchQuery.trim() === '') {
    event.preventDefault();
    errorMessage.textContent = "Введите запрос"; 
  }
});