"""
Generador de PDF para CV Profesional
"""

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import date


def generar_cv_pdf(perfil):
    """
    Genera un PDF profesional del CV
    
    Args:
        perfil: Instancia de PerfilProfesional
    
    Returns:
        BytesIO: Buffer con el PDF generado
    """
    buffer = BytesIO()
    
    # Configuración del documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Contenedor de elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E7D32'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    seccion_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2E7D32'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderPadding=5,
        borderColor=colors.HexColor('#2E7D32'),
        borderRadius=0
    )
    
    texto_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    texto_bold = ParagraphStyle(
        'CustomBold',
        parent=texto_normal,
        fontName='Helvetica-Bold'
    )
    
    # ======================================
    # ENCABEZADO
    # ======================================
    
    # Nombre completo
    nombre = Paragraph(perfil.nombre_completo.upper(), titulo_style)
    elements.append(nombre)
    
    # Título profesional
    titulo = Paragraph(perfil.titulo_profesional, subtitulo_style)
    elements.append(titulo)
    
    # Información de contacto
    contacto_data = [
        [
            Paragraph(f"<b>Email:</b> {perfil.email}", texto_normal),
            Paragraph(f"<b>Teléfono:</b> {perfil.telefono}", texto_normal),
        ],
        [
            Paragraph(f"<b>Ubicación:</b> {perfil.ciudad}, {perfil.pais}", texto_normal),
            Paragraph(f"<b>Experiencia:</b> {perfil.anos_experiencia} años", texto_normal),
        ]
    ]
    
    if perfil.linkedin:
        contacto_data.append([
            Paragraph(f"<b>LinkedIn:</b> {perfil.linkedin}", texto_normal),
            Paragraph(f"<b>GitHub:</b> {perfil.github if perfil.github else 'N/A'}", texto_normal),
        ])
    
    contacto_table = Table(contacto_data, colWidths=[8*cm, 8*cm])
    contacto_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(contacto_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Línea separadora
    linea = Table([['']], colWidths=[16*cm])
    linea.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#2E7D32')),
    ]))
    elements.append(linea)
    
    # ======================================
    # RESUMEN PROFESIONAL
    # ======================================
    
    if perfil.resumen_profesional:
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("RESUMEN PROFESIONAL", seccion_style))
        elements.append(Paragraph(perfil.resumen_profesional, texto_normal))
        elements.append(Spacer(1, 0.3*cm))
    
    # ======================================
    # EXPERIENCIA PROFESIONAL
    # ======================================
    
    experiencias = perfil.experiencias.all()[:10]
    if experiencias.exists():
        elements.append(Paragraph("EXPERIENCIA PROFESIONAL", seccion_style))
        
        for exp in experiencias:
            exp_elementos = []
            
            # Cargo y empresa
            cargo_empresa = Paragraph(
                f"<b>{exp.cargo}</b> - {exp.empresa}",
                texto_bold
            )
            exp_elementos.append(cargo_empresa)
            
            # Fechas y ubicación
            fecha_inicio = exp.fecha_inicio.strftime("%m/%Y")
            fecha_fin = "Presente" if exp.trabajo_actual else exp.fecha_fin.strftime("%m/%Y")
            
            fechas = Paragraph(
                f"{fecha_inicio} - {fecha_fin} | {exp.ciudad}, {exp.pais}",
                ParagraphStyle('dates', parent=texto_normal, fontSize=9, textColor=colors.grey)
            )
            exp_elementos.append(fechas)
            
            # Descripción
            if exp.descripcion:
                desc = Paragraph(exp.descripcion, texto_normal)
                exp_elementos.append(desc)
            
            # Logros
            if exp.logros:
                logros = Paragraph(f"<b>Logros:</b> {exp.logros}", texto_normal)
                exp_elementos.append(logros)
            
            # Tecnologías
            if exp.tecnologias_usadas:
                techs = Paragraph(
                    f"<i>Tecnologías: {exp.tecnologias_usadas}</i>",
                    ParagraphStyle('tech', parent=texto_normal, fontSize=9)
                )
                exp_elementos.append(techs)
            
            exp_elementos.append(Spacer(1, 0.3*cm))
            
            # Agrupar para mantener junto
            elements.append(KeepTogether(exp_elementos))
    
    # ======================================
    # FORMACIÓN ACADÉMICA
    # ======================================
    
    formacion = perfil.formacion_academica.all()[:5]
    if formacion.exists():
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("FORMACIÓN ACADÉMICA", seccion_style))
        
        for edu in formacion:
            edu_elementos = []
            
            # Título e institución
            titulo_edu = Paragraph(
                f"<b>{edu.titulo_obtenido}</b> - {edu.institucion}",
                texto_bold
            )
            edu_elementos.append(titulo_edu)
            
            # Fechas y estado
            fecha_inicio = edu.fecha_inicio.strftime("%m/%Y")
            fecha_fin = edu.fecha_fin.strftime("%m/%Y") if edu.fecha_fin else "En curso"
            
            fechas_edu = Paragraph(
                f"{fecha_inicio} - {fecha_fin} | {edu.get_estado_display()}",
                ParagraphStyle('dates', parent=texto_normal, fontSize=9, textColor=colors.grey)
            )
            edu_elementos.append(fechas_edu)
            
            # Promedio
            if edu.promedio:
                promedio = Paragraph(f"Promedio: {edu.promedio}/10", texto_normal)
                edu_elementos.append(promedio)
            
            # Descripción
            if edu.descripcion:
                desc_edu = Paragraph(edu.descripcion, texto_normal)
                edu_elementos.append(desc_edu)
            
            edu_elementos.append(Spacer(1, 0.3*cm))
            
            elements.append(KeepTogether(edu_elementos))
    
    # ======================================
    # HABILIDADES
    # ======================================
    
    habilidades = perfil.habilidades.all()[:15]
    if habilidades.exists():
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("HABILIDADES", seccion_style))
        
        # Agrupar por tipo
        habilidades_tecnicas = habilidades.filter(tipo='tecnica')
        habilidades_blandas = habilidades.filter(tipo='blanda')
        idiomas = habilidades.filter(tipo='idioma')
        
        if habilidades_tecnicas.exists():
            elements.append(Paragraph("<b>Habilidades Técnicas:</b>", texto_bold))
            skills_tech = ", ".join([f"{h.nombre} ({h.nivel}%)" for h in habilidades_tecnicas])
            elements.append(Paragraph(skills_tech, texto_normal))
            elements.append(Spacer(1, 0.2*cm))
        
        if habilidades_blandas.exists():
            elements.append(Paragraph("<b>Habilidades Blandas:</b>", texto_bold))
            skills_soft = ", ".join([h.nombre for h in habilidades_blandas])
            elements.append(Paragraph(skills_soft, texto_normal))
            elements.append(Spacer(1, 0.2*cm))
        
        if idiomas.exists():
            elements.append(Paragraph("<b>Idiomas:</b>", texto_bold))
            langs = ", ".join([f"{h.nombre} ({h.nivel}%)" for h in idiomas])
            elements.append(Paragraph(langs, texto_normal))
    
    # ======================================
    # PROYECTOS DESTACADOS
    # ======================================
    
    proyectos = perfil.proyectos.filter(destacado=True)[:4]
    if proyectos.exists():
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("PROYECTOS DESTACADOS", seccion_style))
        
        for proy in proyectos:
            proy_elementos = []
            
            # Nombre del proyecto
            nombre_proy = Paragraph(f"<b>{proy.nombre}</b>", texto_bold)
            proy_elementos.append(nombre_proy)
            
            # Descripción
            desc_proy = Paragraph(proy.descripcion_corta, texto_normal)
            proy_elementos.append(desc_proy)
            
            # Tecnologías
            if proy.tecnologias:
                tech_proy = Paragraph(f"<i>Tecnologías: {proy.tecnologias}</i>", texto_normal)
                proy_elementos.append(tech_proy)
            
            # Enlaces
            if proy.url_demo or proy.url_repositorio:
                links = []
                if proy.url_demo:
                    links.append(f"Demo: {proy.url_demo}")
                if proy.url_repositorio:
                    links.append(f"Repo: {proy.url_repositorio}")
                
                enlaces = Paragraph(" | ".join(links), ParagraphStyle('links', parent=texto_normal, fontSize=8))
                proy_elementos.append(enlaces)
            
            proy_elementos.append(Spacer(1, 0.3*cm))
            
            elements.append(KeepTogether(proy_elementos))
    
    # ======================================
    # CERTIFICACIONES
    # ======================================
    
    certificaciones = perfil.certificaciones.all()[:5]
    if certificaciones.exists():
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("CERTIFICACIONES", seccion_style))
        
        for cert in certificaciones:
            cert_elementos = []
            
            # Nombre y entidad
            nombre_cert = Paragraph(
                f"<b>{cert.nombre}</b> - {cert.institucion}",
                texto_bold
            )
            cert_elementos.append(nombre_cert)
            
            # Fecha
            fecha_cert = Paragraph(
                f"Obtenido: {cert.fecha_obtencion.strftime('%m/%Y')}",
                ParagraphStyle('dates', parent=texto_normal, fontSize=9, textColor=colors.grey)
            )
            cert_elementos.append(fecha_cert)
            
            # Código
            if cert.codigo_credencial:
                codigo = Paragraph(f"Credencial: {cert.codigo_credencial}", texto_normal)
                cert_elementos.append(codigo)
            
            cert_elementos.append(Spacer(1, 0.2*cm))
            
            elements.append(KeepTogether(cert_elementos))
    
    # ======================================
    # PIE DE PÁGINA
    # ======================================
    
    elements.append(Spacer(1, 1*cm))
    
    pie = Paragraph(
        f"<i>CV generado el {date.today().strftime('%d/%m/%Y')}</i>",
        ParagraphStyle('footer', parent=texto_normal, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    )
    elements.append(pie)
    
    # ======================================
    # CONSTRUIR PDF
    # ======================================
    
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
