from xhtml2pdf import pisa             # import python module

# Define your data
source_html = "./../deliverable/report_deliv.html"
output_filename = "./../deliverable/report.pdf"

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

# Main program
pisa.showLogging()
convert_html_to_pdf(source_html, output_filename)