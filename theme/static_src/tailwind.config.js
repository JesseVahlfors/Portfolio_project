/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',
        './theme/static/**/*.js',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',
        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                'forest-green': '#2E8B57',
                'terra-cotta': '#E2725B',
                'soft-gray': '#808080',
                'muted-teal': '#5F9EA0',
                'slate-blue': '#6A5ACD',
                'steel-blue': '#4682B4',
                'midnight-blue': '#191970',
                'navy-blue': '#000080',
                'dark-slate-blue': '#483D8B',
                'soft-beige': '#ECE5C7',
            },
            backgroundImage: {
                'main_bg': "url('/static/images/bg4.jpg')",
                'mini_bg': "url('/static/images/bg-mini.jpg')",
            },
            maxWidth: {
                '40': '40rem',
                '60': '60rem',
                '80': '80rem',
                '120': '120rem',
            },
            maxHeight: {
                '40': '40rem',
                '60': '60rem',
                '80': '80rem',
                '120': '120rem',
            },
            minHeight: {
                '60': '60rem',
                '80': '80rem',
                '120': '120rem',
            },
            keyframes: {
                MouseScroll: {
                    '0%': { transform: 'translateY(0)', opacity: '1' }, 
                    '90%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '0' }, 
                },
            },
            animation: {
                MouseScroll: 'MouseScroll 1.5s infinite', 
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
