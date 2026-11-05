/**
 * FramePilot AI — Retention Chart Component
 * Visualizes AI-Predicted Retention vs Measured YouTube Studio Analytics using Chart.js.
 * Redesigned for Sample 3: Dark Professional Video Analysis.
 */

export class RetentionChart {
  constructor(canvasId, onPointClick) {
    this.canvas = document.getElementById(canvasId);
    this.chart = null;
    this.onPointClick = onPointClick;
  }

  render(curveData) {
    if (!this.canvas) return;

    if (this.chart) {
      this.chart.destroy();
    }

    if (!curveData || curveData.length === 0) {
      return;
    }

    const labels = curveData.map(d => `${d.second}s`);
    const predictedValues = curveData.map(d => d.predicted_retention);
    const measuredValues = curveData.map(d => d.measured_retention !== undefined ? d.measured_retention : null);

    const hasMeasured = measuredValues.some(v => v !== null);

    // Sample 3 Color Palette:
    // Electric Blue (#4F8CFF) for predicted risk, Emerald (#38E1A0) for measured channel analytics
    const datasets = [
      {
        label: 'AI-Predicted Retention Risk',
        data: predictedValues,
        borderColor: '#4F8CFF',
        backgroundColor: 'rgba(79, 140, 255, 0.08)',
        borderWidth: 2,
        borderDash: [5, 4],
        fill: true,
        tension: 0.32,
        pointBackgroundColor: '#4F8CFF',
        pointBorderColor: '#07111F',
        pointBorderWidth: 1.5,
        pointRadius: 3.5,
        pointHoverRadius: 6.5
      }
    ];

    if (hasMeasured) {
      datasets.unshift({
        label: 'Measured Channel Retention (YouTube Studio)',
        data: measuredValues,
        borderColor: '#38E1A0',
        backgroundColor: 'rgba(56, 225, 160, 0.08)',
        borderWidth: 2.2,
        fill: true,
        tension: 0.25,
        pointBackgroundColor: '#38E1A0',
        pointBorderColor: '#07111F',
        pointBorderWidth: 1.5,
        pointRadius: 4,
        pointHoverRadius: 7
      });
    }

    const ctx = this.canvas.getContext('2d');
    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false
        },
        onClick: (event, elements) => {
          if (elements.length > 0 && this.onPointClick) {
            const index = elements[0].index;
            const clickedSecond = curveData[index].second;
            this.onPointClick(clickedSecond);
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              color: '#93A4BA',
              font: { family: 'Inter', size: 12, weight: '500' },
              usePointStyle: true,
              boxWidth: 7,
              padding: 16
            }
          },
          tooltip: {
            backgroundColor: '#0D1929',
            titleColor: '#F1F5F9',
            bodyColor: '#93A4BA',
            borderColor: '#243B59',
            borderWidth: 1,
            padding: 10,
            cornerRadius: 6,
            callbacks: {
              label: function(context) {
                return ` ${context.dataset.label}: ${context.parsed.y}%`;
              },
              footer: () => 'Click point to seek video'
            }
          }
        },
        scales: {
          x: {
            grid: {
              color: 'rgba(29, 46, 69, 0.6)',
              drawBorder: false
            },
            ticks: {
              color: '#62768F',
              font: { family: 'JetBrains Mono', size: 11 }
            }
          },
          y: {
            min: 0,
            max: 100,
            grid: {
              color: 'rgba(29, 46, 69, 0.6)',
              drawBorder: false
            },
            ticks: {
              color: '#62768F',
              font: { family: 'JetBrains Mono', size: 11 },
              callback: (val) => `${val}%`,
              stepSize: 20
            }
          }
        }
      }
    });
  }
}
