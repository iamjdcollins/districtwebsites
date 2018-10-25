/* ------------------------------------------------------------------------------
 *
 *  # Custom JS code
 *
 *  Place here all your custom js. Make sure it's loaded after app.js
 *
 * ---------------------------------------------------------------------------- */
window.openPageLoad = function(){
    $.blockUI({ 
        message: '<i class="spinner icon-spinner2" style="font-size: 40px;"></i>',
        baseZ: 999999,
        overlayCSS: {
            backgroundColor: '#1b2024',
            opacity: 0.8,
            cursor: 'wait',
        },
        css: {
            border: 0,
            color: '#fff',
            lineHeight: '40px',
            padding: 0,
            backgroundColor: 'transparent',
            height: '40px',
            width: '40px',
            top: '50%',
            left: '50%',
            marginLeft: '-20px',
            marginTop: '-20px',
        }
    });
}

window.closePageLoad = function(){
    $.unblockUI();
};