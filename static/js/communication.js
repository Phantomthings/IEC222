let loadedCount = 0;
const totalModules = 14;

async function updateModules() {
    try {
        const data = await fetch('/api/communication/modules').then(r => r.json());
        console.log('Data received:', data);

        if (data.modules) {
            for (const [moduleId, status] of Object.entries(data.modules)) {
                const svgObj = document.getElementById(`svg-${moduleId}`);

                if (svgObj && svgObj.contentDocument) {
                    const led = svgObj.contentDocument.getElementById('led-green');

                    if (led) {
                        if (status.fault) {
                            led.setAttribute('fill', 'url(#ledGlowGreen)');
                        } else {
                            led.setAttribute('fill', 'url(#ledGlowRed)');
                        }
                    }
                }
            }
        }
    } catch (e) {
        console.error('Error:', e);
    }
}

for (let i = 1; i <= totalModules; i++) {
    const svgObj = document.getElementById(`svg-M${i}`);
    if (svgObj) {
        svgObj.addEventListener('load', () => {
            loadedCount++;
            if (loadedCount === totalModules) {
                updateModules();
                setInterval(updateModules, 2000);
            }
        });
    }
}
