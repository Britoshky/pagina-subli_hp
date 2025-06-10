document.addEventListener("DOMContentLoaded", function () {
    const chartElement = document.getElementById("growthChart");

    if (chartElement) {
        try {
            // Obtener los datos del atributo data-chart
            const chartData = chartElement.dataset.chart;
            const cumulativeData = JSON.parse(chartData);

            // Validar si los datos están vacíos
            if (!cumulativeData || cumulativeData.length === 0) {
                console.warn("No hay datos para mostrar en el gráfico.");
                return;
            }

            // Extraer fechas y totales
            const dates = cumulativeData.map((entry) => entry.date);
            const totals = cumulativeData.map((entry) => entry.total);

            // Crear el gráfico
            const ctx = chartElement.getContext("2d");
            new Chart(ctx, {
                type: "line",
                data: {
                    labels: dates,
                    datasets: [
                        {
                            label: "Crecimiento Acumulado de Ingresos",
                            data: totals,
                            borderColor: "#1D3557",
                            backgroundColor: "rgba(69, 123, 157, 0.2)",
                            borderWidth: 3,
                            pointBackgroundColor: "#1D3557",
                            pointBorderColor: "#1D3557",
                            pointHoverBackgroundColor: "#A8DADC",
                            pointHoverBorderColor: "#457B9D",
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: "top",
                            labels: {
                                font: {
                                    size: 14,
                                },
                                color: "#333",
                            },
                        },
                        tooltip: {
                            backgroundColor: "#457B9D",
                            titleColor: "#fff",
                            bodyColor: "#fff",
                            borderColor: "#1D3557",
                            borderWidth: 1,
                            callbacks: {
                                label: function (context) {
                                    let value = context.raw.toLocaleString("es-CL", {
                                        style: "currency",
                                        currency: "CLP",
                                        minimumFractionDigits: 0,
                                    });
                                    return `${context.dataset.label}: ${value}`;
                                },
                            },
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Fechas",
                                color: "#333",
                                font: {
                                    size: 14,
                                },
                            },
                            grid: {
                                display: false,
                            },
                            ticks: {
                                color: "#333",
                            },
                            type: "category",
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Total Acumulado (CLP)",
                                color: "#333",
                                font: {
                                    size: 14,
                                },
                            },
                            grid: {
                                color: "rgba(0, 0, 0, 0.1)",
                            },
                            ticks: {
                                color: "#333",
                                callback: function (value) {
                                    return value.toLocaleString("es-CL");
                                },
                            },
                            beginAtZero: true,
                        },
                    },
                },
            });
        } catch (error) {
            console.error("Error al procesar los datos del gráfico:", error);
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("deleteModal");
    const closeButton = document.querySelector(".close");
    let adIdToDelete = 0;

    // Define confirmDeletion globalmente
    window.confirmDeletion = function (id) {
        adIdToDelete = id;
        modal.style.display = "block";
    };

    // Define closeModal globalmente
    window.closeModal = function () {
        modal.style.display = "none";
    };

    if (closeButton) {
        closeButton.onclick = function () {
            window.closeModal();
        };
    }

    window.deleteAd = function () {
        window.location.href = `/ads/delete/${adIdToDelete}`;
    };

    window.onclick = function (event) {
        if (event.target === modal) {
            window.closeModal();
        }
    };
});
