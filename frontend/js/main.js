document.addEventListener('DOMContentLoaded', () => {
    // Получаем параметры из URL (например, ?search=Алтай)
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('search') || '';

    // 1. Поисковая форма (перенаправляет на tours.html с поисковым запросом)
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = document.getElementById('search-input');
            const query = input ? input.value.trim() : '';
            window.location.href = `tours.html?search=${encodeURIComponent(query)}`;
        });
    }

    // 2. Если мы на главной странице (index.html)
    if (document.getElementById('tours-container')) {
        loadTours('tours-container', 3);
    }

    // 3. Если мы на странице всех туров (tours.html)
    if (document.getElementById('all-tours-container')) {
        loadTours('all-tours-container', null, searchQuery);
    }

    // 4. Если мы на странице бронирования (booking.html)
    if (document.getElementById('booking-form')) {
        initBookingPage();
    }
});

/**
 * Загрузка туров из Python REST API (backend-tours)
 */
function loadTours(containerId, limit = null, searchQuery = '') {
    const container = document.getElementById(containerId);

    // Формируем URL с учетом поискового запроса
    let url = '/api/tours';
    if (searchQuery) {
        url += `?search=${encodeURIComponent(searchQuery)}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сети');
            return response.json();
        })
        .then(tours => {
            container.innerHTML = '';

            const toursToShow = limit ? tours.slice(0, limit) : tours;

            if (toursToShow.length === 0) {
                container.innerHTML = `
                    <div style="grid-column: 1/-1; text-align: center; padding: 40px 0;">
                        <h3>По запросу «${searchQuery}» ничего не найдено </h3>
                        <p style="color:#666; margin-top:10px;">Попробуйте ввести другое направление (например: Рим, Египет, Алтай)</p>
                        <a href="tours.html" class="btn btn--book" style="display:inline-block; width:auto; margin-top:15px; text-decoration:none;">Показать все туры</a>
                    </div>
                `;
                return;
            }

            toursToShow.forEach(tour => {
                const cardHtml = `
                    <article class="tour-card">
                        <img src="${tour.image || 'images/tour1.jpg'}" alt="${tour.title}" class="tour-card__image">
                        <div class="tour-card__content">
                            <h3 class="tour-card__title">${tour.title}</h3>
                            <p class="tour-card__desc">${tour.description}</p>
                            <div class="tour-card__meta">
                                <span class="tour-card__price">${Number(tour.price).toLocaleString()} ₽ / чел.</span>
                                <span class="tour-card__rating">${'★'.repeat(tour.stars || 5)}</span>
                            </div>
                            <button class="btn btn--book" onclick="goToBooking(${tour.id})" type="button">Забронировать</button>
                        </div>
                    </article>
                `;
                container.innerHTML += cardHtml;
            });
        })
        .catch(error => {
            console.error('Ошибка загрузки туров:', error);
            container.innerHTML = '<p style="color:red;">Не удалось загрузить туры.</p>';
        });
}

function goToBooking(tourId) {
    window.location.href = `booking.html?tour_id=${tourId}`;
}

function initBookingPage() {
    const selectElement = document.getElementById('tour-select');
    const formElement = document.getElementById('booking-form');
    
    const urlParams = new URLSearchParams(window.location.search);
    const selectedTourId = urlParams.get('tour_id');

    fetch('/api/tours')
        .then(response => response.json())
        .then(tours => {
            selectElement.innerHTML = '<option value="">-- Выберите тур из списка --</option>';

            tours.forEach(tour => {
                const option = document.createElement('option');
                option.value = tour.id;
                option.textContent = `${tour.title} (${Number(tour.price).toLocaleString()} ₽)`;
                
                if (selectedTourId && tour.id == selectedTourId) {
                    option.selected = true;
                }

                selectElement.appendChild(option);
            });
        });

    formElement.addEventListener('submit', (e) => {
        e.preventDefault();
        const alertBox = document.getElementById('booking-alert');
        
        const bookingData = {
            tour_id: selectElement.value,
            user_name: document.getElementById('user-name').value,
            phone: document.getElementById('user-phone').value,
            email: document.getElementById('user-email').value,
            travel_date: document.getElementById('travel-date').value,
            guests_count: document.getElementById('guests-count').value
        };

        fetch('/api/booking', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingData)
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сохранения');
            return response.json();
        })
        .then(data => {
            alertBox.className = 'alert alert--success';
            alertBox.textContent = `Успешно! Ваша заявка №${data.booking_id || ''} принята. Менеджер свяжется с вами.`;
            alertBox.classList.remove('hidden');
            formElement.reset();
        })
        .catch(err => {
            alertBox.className = 'alert alert--danger';
            alertBox.textContent = 'Произошла ошибка при отправке формы.';
            alertBox.classList.remove('hidden');
        });
    });
}