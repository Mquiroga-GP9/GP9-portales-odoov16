# Añade las carpetas "Memorias" y "Otros" a proyectos existentes
Folder = env['documents.folder'].sudo()
Delivery = env['x_project.folder.delivery'].sudo()
Project = env['project.project']

# Detectar automáticamente el campo many2one correcto
o2m_name = 'x_folder_delivery_ids'
inverse_name = Project._fields[o2m_name].inverse_name

# Subcarpetas que deben existir
required_subfolders = ['Planos', 'Actas', 'Aprobaciones', 'Memorias', 'Otros']

for project in records:
    # Obtener la carpeta raíz del proyecto
    project_folder = project.documents_folder_id if 'documents_folder_id' in project._fields else False
    
    if not project_folder:
        continue
    
    # Buscar subcarpetas que ya existen
    existing = Folder.search([
        ('parent_folder_id', '=', project_folder.id),
        ('name', 'in', required_subfolders),
    ])
    
    existing_names = set(existing.mapped('name'))
    
    # Crear las carpetas que faltan
    created_folders = []
    for name in required_subfolders:
        if name not in existing_names:
            new_folder = Folder.create({
                'name': name,
                'parent_folder_id': project_folder.id,
            })
            created_folders.append(new_folder)
    
    # Crear registros de delivery para las nuevas carpetas
    if created_folders:
        # Obtener líneas ya existentes
        existing_folder_ids = set(project.x_folder_delivery_ids.mapped('x_documents_folder_id').ids)
        
        for folder in created_folders:
            if folder.id not in existing_folder_ids:
                Delivery.create({
                    inverse_name: project.id,  # Campo auto-detectado
                    'x_documents_folder_id': folder.id,
                    'x_delivery_status': 'pending',
                })