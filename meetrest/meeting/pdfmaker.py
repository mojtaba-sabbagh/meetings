from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse
from .models import Resolution, Proceeding, Meeting
import arabic_reshaper
from bidi.algorithm import get_display
import io
from jalali_date import date2jalali
PARTICIPANTS_P_LINE = 4
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
    fontName="Yekan" #previously we named our custom font "Yekan"
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
    for i, employee in enumerate(proc.participants.all()):
        parts.append(get_display(arabic_reshaper.reshape(f"{employee.stockholder.first_name} {employee.stockholder.last_name}")))
    return parts

def cerate_proceeding(request, pk):

    storys = []

    resolutions = Resolution.objects.filter(proceeding=pk)
    proc = Proceeding.objects.get(pk=pk)
    title, under_title = proceeding_title(proc)
    parts = proceeding_participants(proc)
    storys.append(Paragraph(get_display(arabic_reshaper.reshape(title)), proceeding_title_style))
    storys.append(Spacer(1,10)) # set the space here
    storys.append(Paragraph(get_display(arabic_reshaper.reshape(under_title)), Titr_text_style))
    
    storys.append(Spacer(1,10))
    storys.append(Spacer(1,10))
    for res in resolutions:
        # reshape the text 
        item_no = get_display(arabic_reshaper.reshape(res.item_no))
        act_text = get_display(arabic_reshaper.reshape(res.act_text))

        # add the text to pdf
        ## dont forget to add the style arabic_text_style
        storys.append(Paragraph(act_text+' .'+item_no, arabic_text_style))
        storys.append(Spacer(1,10)) # set the space here
    
    # Meeting participants
    ps = []
    for i, part in enumerate(parts):
        if (i+1) % PARTICIPANTS_P_LINE == 0:
            storys.append(Spacer(1,10)) # set the space here
            storys.append(Paragraph(spaces.join(ps), arabic_text_style))
            ps = []
        ps.append(part)
    storys.append(Spacer(1,10)) # set the space here
    storys.append(Paragraph(spaces.join(ps), arabic_text_style))


    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize = letter)
    ## add the storys array to the pdf document
    doc.build(storys)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="{mealTime:} by student.pdf"'.format(mealTime='')

    response.write(buffer.getvalue())

    return response