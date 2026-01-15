let svg = null;

document.getElementById('synoptiqueSvg').addEventListener('load', () => {
    svg = document.getElementById('synoptiqueSvg').contentDocument;
    updateData();
    setInterval(updateData, 2000);
});

// Convertir le filtre glow en couleur pour les groupes
function pole_groupe_color(glowFilter) {
    const colorMap = {
        'url(#glowWhite)': '#ffffff',
        'url(#glowGroupGreen)': '#22c55e',
        'url(#glowGroupRed)': '#ef4444',
        'url(#panelGrad)': '#525252'
    };
    return colorMap[glowFilter] || '#525252';
}

async function updateData() {
    if (!svg) return;

    try {
        const response = await fetch('/api/synoptique/data', { cache: "no-store" });
        if (!response.ok) throw new Error('Network error');
        const data = await response.json();

        // Réinitialiser tous les connecteurs de groupes avant la mise à jour
        for (let i = 1; i <= 10; i++) {
            const pdcCircle = svg.getElementById(`G${i}-pdc`);
            const pdcText = svg.getElementById(`G${i}-pdc-text`);
            if (pdcCircle) pdcCircle.setAttribute('fill', '#525252');
            if (pdcText) pdcText.textContent = '-';
        }

        for (const [id, values] of Object.entries(data)) {

            if (id.startsWith('M') && values.vdc !== undefined) {
                const vdcEl = svg.getElementById(`${id}-vdc`);
                if (vdcEl) vdcEl.textContent = values.vdc.toFixed(0);

                const idcEl = svg.getElementById(`${id}-idc`);
                if (idcEl) idcEl.textContent = values.idc.toFixed(0);

                const border = svg.getElementById(`${id}-border`);
                if (border && values.module_color) {
                    border.setAttribute('stroke', values.module_color);
                }
            }

            if (id.startsWith('G') && !id.startsWith('Gl')) {
                const bgRect = svg.getElementById(`${id}-bg`);
                if (bgRect && values.glow_filter) {
                    bgRect.setAttribute('filter', values.glow_filter);
                }

                // Mettre à jour le connecteur du groupe avec le numéro de prise PDC
                if (values.id_prise && values.id_prise >= 1 && values.id_prise <= 4) {
                    // Obtenir la couleur en fonction du status du groupe
                    const groupColor = pole_groupe_color(values.glow_filter);

                    // Mettre à jour le cercle du connecteur de ce groupe (ex: G5-pdc)
                    const pdcCircle = svg.getElementById(`${id}-pdc`);
                    if (pdcCircle) {
                        pdcCircle.setAttribute('fill', groupColor);
                    }

                    // Afficher le numéro de la prise PDC dans le connecteur de ce groupe
                    const pdcText = svg.getElementById(`${id}-pdc-text`);
                    if (pdcText) {
                        pdcText.textContent = values.id_prise.toString();
                    }
                }
            }

            if (id.startsWith('K') && !id.startsWith('KP') && values.is_closed !== undefined) {
                const bg = svg.querySelector(`#${id} rect`);
                if (bg) {
                    bg.setAttribute('stroke', values.border_color);
                    bg.setAttribute('stroke-width', values.is_closed ? '1.5' : '1');
                }

                const contact = svg.getElementById(`${id}-contact`);
                if (contact) {
                    contact.setAttribute('x2', values.contact_x2);
                    contact.setAttribute('y2', values.contact_y2);
                    contact.setAttribute('stroke', values.contact_color);
                }

                const fixed = svg.querySelector(`#${id} line:nth-of-type(2)`);
                if (fixed) {
                    fixed.setAttribute('stroke', values.contact_color);
                }

                const led = svg.getElementById(`${id}-led`);
                if (led) {
                    led.setAttribute('fill', values.led_color);
                    if (values.led_filter !== 'none') {
                        led.setAttribute('filter', values.led_filter);
                    } else {
                        led.removeAttribute('filter');
                    }
                }
            }

            if (id.startsWith('KP') && values.is_closed !== undefined) {
                const bg = svg.getElementById(`${id}-bg`);
                if (bg) {
                    bg.setAttribute('stroke', values.border_color);
                }

                const contact = svg.getElementById(`${id}-contact`);
                if (contact) {
                    contact.setAttribute('x2', values.contact_x2);
                    contact.setAttribute('y2', values.contact_y2);
                    contact.setAttribute('stroke', values.contact_color);
                }

                const fixed = svg.getElementById(`${id}-fixed`);
                if (fixed) {
                    fixed.setAttribute('stroke', values.fixed_color);
                }

                const coil = svg.getElementById(`${id}-coil`);
                if (coil) {
                    coil.setAttribute('stroke', values.coil_color);
                }

                const coilTop = svg.getElementById(`${id}-coil-top`);
                const coilBot = svg.getElementById(`${id}-coil-bot`);
                if (coilTop) coilTop.setAttribute('stroke', values.coil_color);
                if (coilBot) coilBot.setAttribute('stroke', values.coil_color);

                const led = svg.getElementById(`${id}-led`);
                if (led) {
                    led.setAttribute('fill', values.led_color);
                    if (values.led_filter !== 'none') {
                        led.setAttribute('filter', values.led_filter);
                    } else {
                        led.removeAttribute('filter');
                    }
                }
            }

            if (id.startsWith('PDC') && values.color !== undefined) {
                const colorRect = svg.getElementById(`${id}-color`);
                if (colorRect) {
                    colorRect.setAttribute('fill', values.color);
                }

                const connectorCircle = svg.getElementById(`${id}-connector-circle`);
                if (connectorCircle) {
                    connectorCircle.setAttribute('stroke', values.color);
                }

                const statusRect = svg.getElementById(`${id}-status-rect`);
                if (statusRect) {
                    statusRect.setAttribute('stroke', values.color);
                }

                const bodyRect = svg.getElementById(`${id}-body`);
                console.log(`${id}-body:`, bodyRect, 'color:', values.color);
                if (bodyRect) {
                    bodyRect.setAttribute('stroke', values.color);
                }

                const pxCurrentEl = svg.getElementById(`${id}-px-current`);
                if (pxCurrentEl && values.px_current !== undefined) {
                    pxCurrentEl.textContent = ` ${values.px_current} A`;
                }

                const pxVoltageEl = svg.getElementById(`${id}-px-voltage`);
                if (pxVoltageEl && values.px_voltage !== undefined) {
                    pxVoltageEl.textContent = ` ${values.px_voltage} V`;
                }

                const eviVoltageEl = svg.getElementById(`${id}-evi-voltage`);
                if (eviVoltageEl && values.evi_voltage !== undefined) {
                    eviVoltageEl.textContent = ` ${values.evi_voltage} V`;
                }

                const dcbmVoltageEl = svg.getElementById(`${id}-dcbm-voltage`);
                if (dcbmVoltageEl && values.dcbm_voltage !== undefined) {
                    dcbmVoltageEl.textContent = ` ${values.dcbm_voltage} V`;
                }

                const pxPowerEl = svg.getElementById(`${id}-px-power`);
                if (pxPowerEl && values.px_power !== undefined) {
                    pxPowerEl.textContent = `${values.px_power} kW`;
                }

                const modulesRunEl = svg.getElementById(`${id}-modules-run`);
                if (modulesRunEl && values.nb_mxr_running !== undefined) {
                    modulesRunEl.textContent = ` ${values.nb_mxr_running}`;
                }

                const modulesAvailEl = svg.getElementById(`${id}-modules-avail`);
                if (modulesAvailEl && values.nb_mxr_available !== undefined) {
                    modulesAvailEl.textContent = ` ${values.nb_mxr_available}`;
                }

                const led1 = svg.getElementById(`${id}-led1`);
                const led2 = svg.getElementById(`${id}-led2`);
                if (led1) {
                    led1.setAttribute('fill', values.color);
                    if (values.glow_filter !== 'none') {
                        led1.setAttribute('filter', values.glow_filter);
                    } else {
                        led1.removeAttribute('filter');
                    }
                }
                if (led2) {
                    led2.setAttribute('fill', values.color);
                    if (values.glow_filter !== 'none') {
                        led2.setAttribute('filter', values.glow_filter);
                    } else {
                        led2.removeAttribute('filter');
                    }
                }

                const textEl = svg.getElementById(`${id}-text`);
                if (textEl && values.text) {
                    textEl.textContent = values.text;
                }
                if (textEl && values.text_color) {
                    textEl.setAttribute('fill', values.text_color);
                }
            }
        }
    } catch (error) {
        console.error('Erreur mise à jour synoptique:', error);
    }
}
