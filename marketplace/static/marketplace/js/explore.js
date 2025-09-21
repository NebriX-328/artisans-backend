document.addEventListener('DOMContentLoaded', () => {

    const aiQueryTextarea = document.getElementById('ai-query');
    const aiSubmitButton = document.getElementById('ai-submit');
    const aiResponseContainer = document.getElementById('ai-response');

    // Simulate different AI responses for demonstration
    const mockResponses = [
        {
            type: 'products',
            message: 'Here are some handcrafted pottery pieces that match your interest:',
            data: [
                {
                    title: 'Terracotta Handi',
                    price: '₹950',
                    rating: '★★★★☆',
                    image: 'https://images.unsplash.com/photo-1579783900882-c0d3ce7c8b5c?fit=crop&w=400&q=80'
                },
                {
                    title: 'Glazed Ceramic Vase',
                    price: '₹1,500',
                    rating: '★★★★★',
                    image: 'https://images.unsplash.com/photo-1596707323112-c2d96695273f?fit=crop&w=400&q=80'
                },
                {
                    title: 'Painted Clay Pot',
                    price: '₹1,200',
                    rating: '★★★☆☆',
                    image: 'https://images.unsplash.com/photo-1620027788320-96f3c5f470a1?fit=crop&w=400&q=80'
                }
            ]
        },
        {
            type: 'stories',
            message: 'Dive into the stories of these incredible artisans:',
            data: [
                {
                    title: 'The Clay Weaver',
                    description: 'Meet the artisan who is reviving ancient pottery techniques.',
                    link: '#',
                    author: 'By Artisan R',
                    image: 'https://images.unsplash.com/photo-1549419142-3e3e07083f23?fit=crop&w=400&q=80'
                },
                {
                    title: 'Folk Art Narratives',
                    description: 'Discover how one artist is using traditional folk art to tell modern stories.',
                    link: '#',
                    author: 'By Artisan B',
                    image: 'https://images.unsplash.com/photo-1616870028292-6f296c0d87a4?fit=crop&w=400&q=80'
                }
            ]
        }
    ];

    aiSubmitButton.addEventListener('click', () => {
        const query = aiQueryTextarea.value.trim();
        if (query === '') {
            aiResponseContainer.innerHTML = `
                <div class="ai-placeholder">
                    <h3>Please enter your query.</h3>
                    <p>Tell me what you're looking for!</p>
                </div>
            `;
            return;
        }

        // Show a loading state
        aiResponseContainer.innerHTML = `
            <div class="ai-placeholder">
                <div class="loader"></div>
                <h3>Exploring the world of artisans for you...</h3>
            </div>
        `;
        
        // Simulate a delay for the AI response
        setTimeout(() => {
            // Get a random mock response
            const randomIndex = Math.floor(Math.random() * mockResponses.length);
            const response = mockResponses[randomIndex];

            let htmlContent = `<div class="ai-response-message">${response.message}</div>`;

            // Build the HTML based on the response type
            if (response.type === 'products') {
                htmlContent += `<div class="product-grid mt-sp6x">`;
                response.data.forEach(item => {
                    htmlContent += `
                        <div class="product-card">
                            <img src="${item.image}" alt="${item.title}">
                            <div class="product-card-content">
                                <h3>${item.title}</h3>
                                <p class="price">${item.price}</p>
                                <div class="rating">${item.rating}</div>
                                <button class="btn btn-primary btn-add-to-cart">View Product</button>
                            </div>
                        </div>
                    `;
                });
                htmlContent += `</div>`;
            } else if (response.type === 'stories') {
                htmlContent += `<div class="stories-grid mt-sp6x">`;
                response.data.forEach(item => {
                    htmlContent += `
                        <div class="story-card">
                            <img src="${item.image}" alt="${item.title}">
                            <div class="card-content">
                                <h3>${item.title}</h3>
                                <p>${item.description}</p>
                                <a href="${item.link}">${item.author}</a>
                            </div>
                        </div>
                    `;
                });
                htmlContent += `</div>`;
            }

            aiResponseContainer.innerHTML = htmlContent;

        }, 1500); // 1.5 second delay
    });

});