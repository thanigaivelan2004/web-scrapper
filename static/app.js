document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    let searchTerm = document.getElementById('search-term').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `search_term=${searchTerm}`
    })
        .then(response => response.json())
        .then(data => {
            let resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            let chartData = {
                labels: [],
                datasets: []
            };

            let sitePrices = {};
            let allProducts = [];  // Store all products with their unit prices
            let columns = [[], [], []];

            data.forEach((product, index) => {
                let price = parseFloat(product["Discounted Price"].replace(/[^0-9.-]+/g, "")) || parseFloat(product["MRP"].replace(/[^0-9.-]+/g, ""));
                let quantityInfo = product["Quantity"] || '';
                if (!quantityInfo || quantityInfo.toLowerCase() === 'no pack details') {
                    let quantityFromName = extractQuantityFromName(product["Product Name"]);
                    if (quantityFromName) {
                        quantityInfo = quantityFromName;
                    }
                }

                let quantity = parseQuantity(quantityInfo);
                let pricePerUnit = price / quantity.value;
                let site = product["Site"];

                // Store product with its unit price for recommendations
                allProducts.push({
                    ...product,
                    pricePerUnit,
                    quantityInfo,
                    unitType: quantity.unit
                });

                if (!sitePrices[site]) {
                    sitePrices[site] = [];
                }
                sitePrices[site].push(pricePerUnit);

                let productCard = `
                    <div class="product-card card mb-3 h-100">
                        <div class="card-body">
                            <h5 class="card-title">${product["Product Name"]}</h5>
                            <p class="card-text">Quantity: ${quantityInfo}</p>
                            <p class="card-text">MRP: ${product["MRP"]}</p>
                            <p class="card-text">Discounted Price: ${product["Discounted Price"] || 'N/A'}</p>
                            <p class="card-text">Price per ${quantity.unit}: ₹${pricePerUnit.toFixed(2)}</p>
                            <p class="card-text">Offer: ${product["Offer"]}</p>
                            <p class="card-text">Company Name: ${product["Company Name"]}</p>
                            <img src="${product["Image URL"]}" class="img-fluid mb-2" alt="${product["Product Name"]}">
                            <p class="card-text">Site: ${product["Site"]}</p>
                            <a href="${product["Product Link"]}" class="btn btn-primary" target="_blank">View Product</a>
                        </div>
                    </div>
                `;

                columns[index % 3].push(productCard);
                chartData.labels.push(index + 1);
            });

            // Display product cards in columns
            let maxColumnLength = Math.max(columns[0].length, columns[1].length, columns[2].length);
            for (let i = 0; i < maxColumnLength; i++) {
                let row = document.createElement('div');
                row.classList.add('row');

                for (let j = 0; j < 3; j++) {
                    let colDiv = document.createElement('div');
                    colDiv.classList.add('col-md-4');
                    colDiv.innerHTML = columns[j][i] || '';
                    row.appendChild(colDiv);
                }

                resultsDiv.appendChild(row);
            }

            // Create and display chart
            chartData.datasets = Object.entries(sitePrices).map(([site, prices]) => ({
                label: site,
                data: prices,
                backgroundColor: getRandomColor()
            }));

            let ctx = document.getElementById('comparison-chart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: chartData,
                options: {
                    responsive: true,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    let pricePerUnit = tooltipItem.raw.toFixed(2);
                                    return `₹${pricePerUnit} per g/ml`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Price per Unit (g/ml)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Products'
                            }
                        }
                    }
                }
            });

            // Add recommendations section
            displayRecommendations(allProducts);

            // Calculate average price per unit
            let totalPricePerUnit = allProducts.reduce((sum, product) => sum + product.pricePerUnit, 0);
            let averagePricePerUnit = totalPricePerUnit / allProducts.length;

            // Create and display the new product card
            let sampleProduct = allProducts[0];
            let newProduct = {
                title: "Sample Product",
                quantity: "1 L / 1 g",
                mrp: (1000 * averagePricePerUnit).toFixed(2),
                discountedPrice: (1000 * averagePricePerUnit).toFixed(2),
                pricePerUnit: averagePricePerUnit.toFixed(2),
                offer: "Best Value",
                companyName: "MyWebsite",
                imageUrl: sampleProduct["Image URL"],
                site: "MyWebsite"
            };

            let newProductCard = `
                <div class="product-card card mb-3 h-100" style="margin: auto; max-width: 400px;">
                    <div class="card-body">
                        <h5 class="card-title">${newProduct.title}</h5>
                        <p class="card-text">Quantity: ${newProduct.quantity}</p>
                        <p class="card-text">MRP: ₹${newProduct.mrp}</p>
                        <label for="discounted-price">Discounted Price (₹):</label>
                        <input type="number" id="discounted-price" class="form-control mb-2" value="${newProduct.discountedPrice}">
                        <p class="card-text">Price per unit: <span id="price-per-unit">₹${newProduct.pricePerUnit}</span></p>
                        <p class="card-text"><span id="price-rating" class="badge bg-success">Good</span></p>
                        <p class="card-text">Company Name: ${newProduct.companyName}</p>
                        <img src="${newProduct.imageUrl}" class="img-fluid mb-2" alt="Sample Product">
                        <p class="card-text">Site: ${newProduct.site}</p>
                        <a href="#" class="btn btn-primary" target="_blank">View Product</a>
                        <button id="save-product" class="btn btn-secondary mt-2">Save</button>
                    </div>
                </div>
            `;
            resultsDiv.insertAdjacentHTML('beforeend', newProductCard);

            // Add event listener to the discounted price input
            document.getElementById('discounted-price').addEventListener('input', function () {
                let discountedPrice = parseFloat(this.value);
                let pricePerUnit = discountedPrice / 1000;
                document.getElementById('price-per-unit').innerText = `₹${pricePerUnit.toFixed(2)}`;
                if (pricePerUnit > averagePricePerUnit) {
                    document.getElementById('price-rating').innerText = 'Poor';
                    document.getElementById('price-rating').classList.remove('bg-success');
                    document.getElementById('price-rating').classList.add('bg-danger');
                } else {
                    document.getElementById('price-rating').innerText = 'Good';
                    document.getElementById('price-rating').classList.remove('bg-danger');
                    document.getElementById('price-rating').classList.add('bg-success');
                }
                // Update the newProduct object
                newProduct.discountedPrice = discountedPrice.toFixed(2);
                newProduct.pricePerUnit = pricePerUnit.toFixed(2);
            });

            // Add event listener to the save button
            document.getElementById('save-product').addEventListener('click', function () {
                let dataStr = JSON.stringify(newProduct, null, 2);
                let dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

                let exportFileDefaultName = 'product.json';

                let linkElement = document.createElement('a');
                linkElement.setAttribute('href', dataUri);
                linkElement.setAttribute('download', exportFileDefaultName);
                linkElement.click();
            });
        });
});

function displayRecommendations(products) {
    // Group products by unit type (g, ml, etc.)
    let groupedProducts = {};
    products.forEach(product => {
        if (!groupedProducts[product.unitType]) {
            groupedProducts[product.unitType] = [];
        }
        groupedProducts[product.unitType].push(product);
    });

    // Create recommendations div
    let recommendationsDiv = document.createElement('div');
    recommendationsDiv.classList.add('recommendations', 'mt-4');
    recommendationsDiv.innerHTML = '<h2 class="mb-4">Recommended Products (Best Value)</h2>';

    // Process each unit type group
    Object.entries(groupedProducts).forEach(([unitType, unitProducts]) => {
        // Sort products by price per unit
        let sortedProducts = unitProducts.sort((a, b) => a.pricePerUnit - b.pricePerUnit);
        // Take top 3 best value products
        let bestProducts = sortedProducts.slice(0, 3);

        if (bestProducts.length > 0) {
            let unitSection = document.createElement('div');
            unitSection.innerHTML = `<h3 class="mb-3">Best Value ${unitType.toUpperCase()} Products</h3>`;
            
            let row = document.createElement('div');
            row.classList.add('row');

            bestProducts.forEach(product => {
                let col = document.createElement('div');
                col.classList.add('col-md-4');
                col.innerHTML = `
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${product["Product Name"]}</h5>
                            <p class="card-text">
                                <span class="badge bg-success">Best Value!</span><br>
                                Price per ${unitType}: ₹${product.pricePerUnit.toFixed(2)}<br>
                                Quantity: ${product.quantityInfo}<br>
                                Site: ${product["Site"]}
                            </p>
                            <a href="${product["Product Link"]}" class="btn btn-primary" target="_blank">View Deal</a>
                        </div>
                    </div>
                `;
                row.appendChild(col);
            });

            unitSection.appendChild(row);
            recommendationsDiv.appendChild(unitSection);
        }
    });

    // Add recommendations to the page
    document.getElementById('results').appendChild(recommendationsDiv);
}

function parseQuantity(quantity) {
    let multiplier = 1;
    let multiMatch = quantity.match(/(\d+\.?\d*)\s*[xX]\s*(\d+\.?\d*)\s*(kg|g|l|ml|unit)/i);
    if (multiMatch) {
        multiplier = parseFloat(multiMatch[1]);
        let value = parseFloat(multiMatch[2]);
        let unit = multiMatch[3].toLowerCase();
        if (unit === 'ml') {
            return { value: value * multiplier, unit: 'ml' };
        } else if (unit === 'l') {
            return { value: value * 1000 * multiplier, unit: 'ml' };
        } else if (unit === 'kg') {
            return { value: value * 1000 * multiplier, unit: 'g' };
        } else if (unit === 'g') {
            return { value: value * multiplier, unit: 'g' };
        } else {
            return { value: multiplier, unit: 'unit' };
        }
    } else {
        let value = parseFloat(quantity.replace(/[^0-9.-]+/g, ""));
        if (quantity.toLowerCase().includes('ml')) {
            return { value: value, unit: 'ml' };
        } else if (quantity.toLowerCase().includes('l')) {
            return { value: value * 1000, unit: 'ml' };
        } else if (quantity.toLowerCase().includes('kg')) {
            return { value: value * 1000, unit: 'g' };
        } else if (quantity.toLowerCase().includes('g')) {
            return { value: value, unit: 'g' };
        } else {
            return { value: 1, unit: 'unit' };
        }
    }
}


function extractQuantityFromName(productName) {
    let match = productName.match(/(\d+\.?\d*)\s*(kg|g|l|ml)/i);
    if (match) {
        return `${match[1]} ${match[2]}`;
    }
    return null;
}

function getRandomColor() {
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}