"""
Definición centralizada de parámetros predeterminados del sitio.
Esto permite mantener consistencia entre migraciones, context processors y el panel admin.
"""

DEFAULT_PARAMETERS = [
    # Empresa y Contacto (Existentes)
    {
        'key': 'COMPANY_NAME',
        'label': 'Nombre de la Empresa',
        'value': 'Kokori',
        'description': 'Nombre que aparecerá en el título del sitio y branding.'
    },
    {
        'key': 'COMPANY_ICON_LETTER',
        'label': 'Letra del Icono',
        'value': 'K',
        'description': 'Letra individual que se muestra en el icono circular del logo.'
    },
    {
        'key': 'FOOTER_COPYRIGHT',
        'label': 'Texto de Copyright',
        'value': '&copy; 2024 Kokori Broaster',
        'description': 'Texto que aparece en la parte inferior de todas las páginas.'
    },
    {
        'key': 'CONTACT_PHONE',
        'label': 'Teléfono de Contacto',
        'value': '+1 234 567 890',
        'description': 'Número de teléfono principal para clientes.'
    },
    {
        'key': 'CONTACT_EMAIL',
        'label': 'Email de Contacto',
        'value': 'contacto@kokori.com',
        'description': 'Correo electrónico principal para consultas.'
    },
    {
        'key': 'ADDRESS',
        'label': 'Dirección Física',
        'value': 'Calle Principal #123',
        'description': 'Dirección del local principal.'
    },
    
    # Redes Sociales (Existentes)
    {
        'key': 'SOCIAL_FACEBOOK',
        'label': 'URL Facebook',
        'value': '#',
        'description': 'Enlace a la página de Facebook.'
    },
    {
        'key': 'SOCIAL_INSTAGRAM',
        'label': 'URL Instagram',
        'value': '#',
        'description': 'Enlace al perfil de Instagram.'
    },
    {
        'key': 'SOCIAL_TIKTOK',
        'label': 'URL TikTok',
        'value': '#',
        'description': 'Enlace al perfil de TikTok.'
    },

    # --- NUEVOS PARÁMETROS PARA HOME PAGE ---
    
    # Hero Section
    {
        'key': 'HOME_HERO_BADGE',
        'label': 'Home: Texto del Badge Hero',
        'value': 'El sabor que define la tradición',
        'description': 'Texto pequeño que aparece sobre el título principal en el Home.'
    },
    {
        'key': 'HOME_HERO_TITLE_1',
        'label': 'Home: Título Hero Parte 1',
        'value': 'Crujiente. Dorado.',
        'description': 'Primera parte del título principal en el Home.'
    },
    {
        'key': 'HOME_HERO_TITLE_2',
        'label': 'Home: Título Hero Parte 2',
        'value': 'Simplemente Perfecto.',
        'description': 'Segunda parte del título (con color degradado) en el Home.'
    },
    {
        'key': 'HOME_HERO_DESCRIPTION',
        'label': 'Home: Descripción Hero',
        'value': 'Seleccionamos los mejores cortes y especias para ofrecerte una experiencia gastronómica única en cada bocado.',
        'description': 'Párrafo descriptivo debajo del título principal en el Home.'
    },
    {
        'key': 'HOME_HERO_IMAGE',
        'label': 'Home: Imagen de Experiencia',
        'value': '',
        'image': 'settings/kokori_experience_hero.png',
        'description': 'Imagen que representa la experiencia Kokori en la sección Hero.'
    },
    
    # Botones de Acción
    {
        'key': 'HOME_CTA_ORDER_TEXT',
        'label': 'Home: Texto Botón Pedido',
        'value': 'Hacer Pedido',
        'description': 'Texto del botón principal de acción en el Hero.'
    },
    {
        'key': 'HOME_CTA_MENU_TEXT',
        'label': 'Home: Texto Botón Menú',
        'value': 'Explorar Menú',
        'description': 'Texto del botón secundario para ver el menú.'
    },
    
    # Ratings
    {
        'key': 'HOME_RATINGS_LABEL',
        'label': 'Home: Etiqueta de Calificaciones',
        'value': 'Calificaciones',
        'description': 'Texto que aparece debajo del contador de calificaciones.'
    },

    # Sección de Compromiso (Specialties)
    {
        'key': 'HOME_COMMITMENT_SUBTITLE',
        'label': 'Home: Subtítulo de Compromiso',
        'value': 'El Sello de Calidad',
        'description': 'Texto pequeño sobre el título de la sección de compromiso.'
    },
    {
        'key': 'HOME_COMMITMENT_TITLE',
        'label': 'Home: Título de Compromiso',
        'value': 'Nuestro Compromiso',
        'description': 'Título principal de la sección de especialidades.'
    },
    
    # Especialidades
    {
        'key': 'HOME_SPECIALTY_1_TITLE',
        'label': 'Home: Especialidad 1 Título',
        'value': 'Receta de Autor',
        'description': 'Título de la primera tarjeta de especialidad.'
    },
    {
        'key': 'HOME_SPECIALTY_1_DESC',
        'label': 'Home: Especialidad 1 Descripción',
        'value': 'Nuestra mezcla exclusiva de especias crea un sabor inconfundible y superior.',
        'description': 'Descripción de la primera tarjeta de especialidad.'
    },
    {
        'key': 'HOME_SPECIALTY_2_TITLE',
        'label': 'Home: Especialidad 2 Título',
        'value': 'Máxima Frescura',
        'description': 'Título de la segunda tarjeta de especialidad.'
    },
    {
        'key': 'HOME_SPECIALTY_2_DESC',
        'label': 'Home: Especialidad 2 Descripción',
        'value': 'Pollo de granja seleccionado diariamente para garantizar frescura en cada plato.',
        'description': 'Descripción de la segunda tarjeta de especialidad.'
    },
    {
        'key': 'HOME_SPECIALTY_3_TITLE',
        'label': 'Home: Especialidad 3 Título',
        'value': 'Servicio Ágil',
        'description': 'Título de la tercera tarjeta de especialidad.'
    },
    {
        'key': 'HOME_SPECIALTY_3_DESC',
        'label': 'Home: Especialidad 3 Descripción',
        'value': 'Procesos optimizados para que disfrutes de tu pedido siempre caliente y al instante.',
        'description': 'Descripción de la tercera tarjeta de especialidad.'
    },

    # CTA Final
    {
        'key': 'HOME_FINAL_CTA_TITLE_1',
        'label': 'Home: Final CTA Título 1',
        'value': '¿Listo para',
        'description': 'Primera parte del título en la sección final de CTA.'
    },
    {
        'key': 'HOME_FINAL_CTA_TITLE_2',
        'label': 'Home: Final CTA Título 2',
        'value': 'repetir la experiencia?',
        'description': 'Segunda parte del título (color naranja) en la sección final.'
    },
    {
        'key': 'HOME_FINAL_CTA_DESC',
        'label': 'Home: Final CTA Descripción',
        'value': 'Únete y accede a beneficios exclusivos.',
        'description': 'Texto descriptivo en la sección final de CTA.'
    },
    {
        'key': 'HOME_FINAL_CTA_BUTTON',
        'label': 'Home: Final CTA Botón',
        'value': '¡Ordenar Ahora!',
        'description': 'Texto del botón de acción en la sección final.'
    },
]
