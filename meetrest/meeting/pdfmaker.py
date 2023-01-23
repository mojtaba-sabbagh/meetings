from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from .models import Resolution, Proceeding, Meeting
import arabic_reshaper
from bidi.algorithm import get_display
import io
from jalali_date import date2jalali
from textwrap import wrap

PARTICIPANTS_P_LINE = 5
spaces = '&nbsp;'*30

pdfmetrics.registerFont(TTFont('Yekan', '../fonts/Yekan/Yekan.ttf'))
pdfmetrics.registerFont(TTFont('Titr', '../fonts/Titr/titr.ttf'))

#init the style sheet
styles = getSampleStyleSheet()
arabic_text_style = ParagraphStyle(
    'border', # border on
    parent = styles['Normal'] , # Normal is a defaul style  in  getSampleStyleSheet
    #borderColor= '#333333',
    #borderWidth =  1,
    #borderPadding  =  2,
    rightIndent = 30,
    alignment = 2,
    wordWrap = None,
    fontName="Yekan", #previously we named our custom font "Yekan"
    fontSize=9,
)
participants_text_style = ParagraphStyle(
    'border', # border on
    parent = styles['Normal'] , # Normal is a defaul style  in  getSampleStyleSheet
    #borderColor= '#333333',
    #borderWidth =  1,
    #borderPadding  =  2,
    rightIndent = 30,
    alignment = 1,
    wordWrap = None,
    fontName="Yekan", #previously we named our custom font "Yekan"
    fontSize=8,
)
Titr_text_style = ParagraphStyle(
    'border', # border on
    parent = styles['Normal'] , # Normal is a defaul style  in  getSampleStyleSheet
    #borderColor= '#333333',
    #borderWidth =  1,
    #borderPadding  =  2,
    spaceAfter = 5,
    rightIndent = 30,
    alignment = 2,
    fontName="Titr" #previously we named our custom font "Yekan"
)
proceeding_title_style = ParagraphStyle(
    'border', # border on
    parent = styles['Normal'] , # Normal is a defaul style  in  getSampleStyleSheet
    #borderColor= '#333333',
    #borderWidth =  1,
    #borderPadding  =  2,
    spaceBefore = 5,
    spaceAfter = 15,
    alignment = 1,
    fontName="Titr" #previously we named our custom font "Yekan"
)

def proceeding_title(proc):
    meeting = Meeting.objects.get(pk=proc.meeting.id)
    title = f"<b>صورتجلسه شماره {proc.proceeding_no} {meeting.meeting_name} به تاریخ {date2jalali(proc.pdate).strftime('%Y/%m/%d')}</b>"
    under_title = f"این جلسه با حضور شرکت کنندگان زیر در ساعت {proc.ptime.strftime('%H:%M')} برگزار شد و مفاد ذیل به تصویب رسید."
    return title, under_title

def proceeding_participants(proc):
    parts = []
    positions = []
    for i, employee in enumerate(proc.participants.all()):
        parts.append(get_display(arabic_reshaper.reshape(f"{employee.stockholder.first_name} {employee.stockholder.last_name}")))
        positions.append(get_display(arabic_reshaper.reshape(employee.position)))
    return parts, positions

def cerate_proceeding(request, pk):

    storys = []

    resolutions = Resolution.objects.filter(proceeding=pk)
    proc = Proceeding.objects.get(pk=pk)
    title, under_title = proceeding_title(proc)
    parts, positions = proceeding_participants(proc)
    storys.append(Paragraph(get_display(arabic_reshaper.reshape(title)), proceeding_title_style))
    storys.append(Spacer(1,10)) # set the space here
    storys.append(Paragraph(get_display(arabic_reshaper.reshape(under_title)), Titr_text_style))
    
    storys.append(Spacer(1,10))
    storys.append(Spacer(1,10))
    for res in resolutions:
        # reshape the text 
        #item_no = get_display(arabic_reshaper.reshape(res.item_no))
        act_text = f"{res.item_no}. {res.act_text}"
        lines = wrap(act_text, 120)
        for line in lines:    
            # add the text to pdf
            ## dont forget to add the style arabic_text_style
            line = get_display(arabic_reshaper.reshape(line))
            storys.append(Paragraph(line, arabic_text_style))
        storys.append(Spacer(1,10)) # set the space here

    # Meeting participants
    ps = []
    pos_line = []
    rows =[]
    tableStyle = TableStyle ([
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (-1, -1), 'Yekan'),
            ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'), # hours c1 l1,2
            ])
    for i, part in enumerate(parts):
        if (i+1) % PARTICIPANTS_P_LINE == 0:
            rows.append(ps)
            rows.append(pos_line)
            rows.append([])
            ps = []
            pos_line = []
        ps.append(Paragraph(part, participants_text_style))
        pos_line.append(Paragraph(positions[i], participants_text_style))
    
    storys.append(Spacer(1,10)) # set the space here
    storys.append(Spacer(1,10)) # set the space here
    storys.append(Spacer(1,10)) # set the space here

    rows.append(ps)
    rows.append(pos_line)
    table = Table(rows, colWidths=130, rowHeights=10)
    table.setStyle(tableStyle)
    storys.append(table)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize = A4)
    ## add the storys array to the pdf document
    doc.build(storys)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="{mealTime:} by student.pdf"'.format(mealTime='')

    response.write(buffer.getvalue())

    return response