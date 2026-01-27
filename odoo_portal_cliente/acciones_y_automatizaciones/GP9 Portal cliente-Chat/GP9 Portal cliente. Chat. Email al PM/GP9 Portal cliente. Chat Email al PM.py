# GP9 Portal: Email al PM cuando cliente envía mensaje
for record in records:
    project = record.x_project_id
    if not project:
        continue
    
    pms = project.x_studio_many2many_field_0UY78
    if not pms:
        continue
    
    client_name = project.partner_id.name or 'Cliente'
    project_name = project.name or 'Proyecto'
    message_text = record.x_message or ''
    
    base_url = env['ir.config_parameter'].sudo().get_param('web.base.url')
    project_url = f"{base_url}/web#id={project.id}&model=project.project&view_type=form"
    
    html_body = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 560px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">
        
        <div style="background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%); padding: 28px 32px;">
            <h1 style="color: #ffffff; margin: 0; font-size: 18px; font-weight: 600;">
                ¡Nuevo mensaje de cliente!
            </h1>
        </div>
        
        <div style="padding: 32px;">
            <p style="color: #4a5568; font-size: 15px; line-height: 1.6; margin: 0 0 24px 0;">
                Has recibido un nuevo mensaje en el portal de cliente.
            </p>
            
            <div style="background-color: #f7fafc; border-left: 3px solid #2d3748; padding: 20px 24px; border-radius: 0 8px 8px 0; margin-bottom: 28px;">
                <p style="margin: 0 0 12px 0; font-size: 14px; color: #718096;">
                    <strong style="color: #2d3748;">Proyecto:</strong> {project_name}
                </p>
                <p style="margin: 0 0 12px 0; font-size: 14px; color: #718096;">
                    <strong style="color: #2d3748;">Cliente:</strong> {client_name}
                </p>
                <p style="margin: 16px 0 0 0; font-size: 14px; color: #2d3748; line-height: 1.6;">
                    <strong>Mensaje:</strong><br>
                    <span style="color: #4a5568;">"{message_text}"</span>
                </p>
            </div>
            
            <a href="{project_url}" style="display: inline-block; background-color: #2d3748; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-size: 14px; font-weight: 600;">
                Ver proyecto
            </a>
        </div>
        
        <div style="background-color: #f7fafc; padding: 20px 32px; border-top: 1px solid #e2e8f0;">
            <p style="color: #a0aec0; font-size: 12px; margin: 0; text-align: center;">
                GP9 · Portal Cliente
            </p>
        </div>
        
    </div>
    """
    
    for pm in pms:
        pm_email = pm.work_email
        if not pm_email:
            continue
        
        mail_values = {
            'subject': f'Portal Cliente: Nuevo mensaje de {client_name} en {project_name}',
            'body_html': html_body,
            'email_to': pm_email,
            'email_from': env.company.email or 'comunicacio@gp9consulting.com',
            'auto_delete': True,
        }
        mail = env['mail.mail'].sudo().create(mail_values)
        mail.send()