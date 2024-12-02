const URL = 'http://localhost:8010/api/image_folder';

export const getUserApi = () =>
  fetch(`${URL}/users/`)
    .then((res) => {
      console.log('Ответ сервера:', res);
      return res.json();
    })
    .then((data) => {
      console.log('Полученные данные:', data);
      return data;
    })
    .catch((err) => {
      console.error('Ошибка:', err);
    });
