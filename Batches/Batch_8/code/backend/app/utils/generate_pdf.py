import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Industrial IoT Telemetry Compression & Optimization Platform — Mathematical Specification")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — ACADEMIC & ENGINEERING REFERENCE")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)
        self.restoreState()

def generate_pdf(output_path="docs/MATHEMATICAL_SPECIFICATION.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    formula_style = ParagraphStyle(
        'Formula_Custom',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=3,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1e293b")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("MATHEMATICAL SPECIFICATION", title_style))
    story.append(Paragraph("Industrial IoT Telemetry Compression & Network Optimization Platform", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=10))

    meta_data = [
        [
            Paragraph("<b>Author:</b> Senior Algorithm Engineer & Systems Architect", meta_style),
            Paragraph("<b>Date:</b> March 2025", meta_style),
            Paragraph("<b>Target Network:</b> 9.6 kbps Sub-GHz Link", meta_style)
        ],
        [
            Paragraph("<b>Sensor Population:</b> 5,000 Edge Nodes", meta_style),
            Paragraph("<b>Traffic Rate:</b> 40 messages/second", meta_style),
            Paragraph("<b>Hardware Limit:</b> 4-bit Code Register", meta_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 160, 174])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1
    story.append(Paragraph("1. Problem Definition & Architectural Context", h1_style))
    story.append(Paragraph(
        "Industrial IoT gateways aggregate periodic and interrupt-driven telemetry from extensive field sensor networks (5,000 sensors) "
        "and transmit status frames across narrowband communication channels. The physical link is constrained to a 9,600 bits per second (9.6 kbps) "
        "transmission capacity. Under legacy architectures, 8 discrete sensor status codes are transmitted using a uniform fixed-length 3-bit binary encoding "
        "(log2(8) = 3 bits/message). Fixed-length encoding squanders network capacity by dedicating the same bandwidth to rare critical alerts as to frequent nominal pulses.",
        body_style
    ))
    story.append(Paragraph(
        "To maximize network headroom, the gateway constructs an optimal variable-length prefix-free code using empirical frequencies. "
        "However, edge receiver microcontrollers (e.g., ARM Cortex-M0+, PIC24) possess strict 4-bit register boundaries. Codewords exceeding 4 bits "
        "overflow hardware registers, requiring length-limited prefix code synthesis.",
        body_style
    ))

    # Section 2
    story.append(Paragraph("2. Input Data, Empirical Distribution & Axiom Validation", h1_style))
    story.append(Paragraph(
        "The empirical status frequency distribution observed over a calibrated one-hour window across 5,000 sensors is summarized below. "
        "The aggregate telemetry generation rate is exactly 40 messages/second across the entire network.",
        body_style
    ))

    dist_table_data = [
        [Paragraph("Symbol", table_cell_header), Paragraph("Frequency (per 100)", table_cell_header), Paragraph("Probability p(i)", table_cell_header), Paragraph("Semantic", table_cell_header)],
        [Paragraph("OK", table_cell_bold), Paragraph("52", table_cell), Paragraph("0.5200", table_cell), Paragraph("Nominal normal operation", table_cell)],
        [Paragraph("TEMP_HI", table_cell_bold), Paragraph("14", table_cell), Paragraph("0.1400", table_cell), Paragraph("High temperature alert", table_cell)],
        [Paragraph("TEMP_LO", table_cell_bold), Paragraph("11", table_cell), Paragraph("0.1100", table_cell), Paragraph("Low temperature alert", table_cell)],
        [Paragraph("HUM", table_cell_bold), Paragraph("9", table_cell), Paragraph("0.0900", table_cell), Paragraph("Humidity threshold exceeded", table_cell)],
        [Paragraph("VIB", table_cell_bold), Paragraph("7", table_cell), Paragraph("0.0700", table_cell), Paragraph("Excess vibration alert", table_cell)],
        [Paragraph("DOOR", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.0400", table_cell), Paragraph("Enclosure door open", table_cell)],
        [Paragraph("FAULT", table_cell_bold), Paragraph("2", table_cell), Paragraph("0.0200", table_cell), Paragraph("Inverter fault trip", table_cell)],
        [Paragraph("RESET", table_cell_bold), Paragraph("1", table_cell), Paragraph("0.0100", table_cell), Paragraph("Watchdog reset pulse", table_cell)],
        [Paragraph("TOTAL", table_cell_header), Paragraph("100", table_cell_header), Paragraph("1.0000", table_cell_header), Paragraph("Validated Probability Axiom", table_cell_header)],
    ]
    t1 = Table(dist_table_data, colWidths=[90, 110, 110, 194])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#0f172a")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t1)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Shannon Entropy Lower Bound:</b> H(X) = - Σ p_i log2(p_i) = <b>2.1843 bits/message</b>. "
        "No lossless prefix-free code can achieve an average code length below this theoretical entropy limit.",
        body_style
    ))

    # Section 3
    story.append(Paragraph("3. Optimal Huffman Coding & Mathematical Optimality Proof", h1_style))
    story.append(Paragraph(
        "Using a min-heap priority queue, Huffman merges the two minimum-weight nodes iteratively: "
        "(1+2=3) -> (3+4=7) -> (7+7=14) -> (9+11=20) -> (14+14=28) -> (20+28=48) -> (48+52=100 Root).",
        body_style
    ))

    huff_table_data = [
        [Paragraph("Symbol", table_cell_header), Paragraph("Freq", table_cell_header), Paragraph("Codeword", table_cell_header), Paragraph("Length (bits)", table_cell_header), Paragraph("p(i) * l(i)", table_cell_header), Paragraph("Register <= 4 bits", table_cell_header)],
        [Paragraph("OK", table_cell_bold), Paragraph("52", table_cell), Paragraph("1", table_cell_bold), Paragraph("1", table_cell), Paragraph("0.5200", table_cell), Paragraph("PASS", table_cell)],
        [Paragraph("TEMP_HI", table_cell_bold), Paragraph("14", table_cell), Paragraph("010", table_cell_bold), Paragraph("3", table_cell), Paragraph("0.4200", table_cell), Paragraph("PASS", table_cell)],
        [Paragraph("TEMP_LO", table_cell_bold), Paragraph("11", table_cell), Paragraph("001", table_cell_bold), Paragraph("3", table_cell), Paragraph("0.3300", table_cell), Paragraph("PASS", table_cell)],
        [Paragraph("HUM", table_cell_bold), Paragraph("9", table_cell), Paragraph("000", table_cell_bold), Paragraph("3", table_cell), Paragraph("0.2700", table_cell), Paragraph("PASS", table_cell)],
        [Paragraph("VIB", table_cell_bold), Paragraph("7", table_cell), Paragraph("0110", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.2800", table_cell), Paragraph("PASS", table_cell)],
        [Paragraph("DOOR", table_cell_bold), Paragraph("4", table_cell), Paragraph("01111", table_cell_bold), Paragraph("5", table_cell), Paragraph("0.2000", table_cell), Paragraph("FAIL (> 4 bits)", table_cell_bold)],
        [Paragraph("FAULT", table_cell_bold), Paragraph("2", table_cell), Paragraph("011101", table_cell_bold), Paragraph("6", table_cell), Paragraph("0.1200", table_cell), Paragraph("FAIL (> 4 bits)", table_cell_bold)],
        [Paragraph("RESET", table_cell_bold), Paragraph("1", table_cell), Paragraph("011100", table_cell_bold), Paragraph("6", table_cell), Paragraph("0.0600", table_cell), Paragraph("FAIL (> 4 bits)", table_cell_bold)],
        [Paragraph("AVERAGE / TOTAL", table_cell_header), Paragraph("100", table_cell_header), Paragraph("Kraft = 1.000", table_cell_header), Paragraph("Max = 6", table_cell_header), Paragraph("L = 2.2000", table_cell_header), Paragraph("HARDWARE VIOLATION", table_cell_header)],
    ]
    t2 = Table(huff_table_data, colWidths=[80, 45, 90, 75, 80, 134])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#dc2626")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Huffman Optimality Proof:</b> Follows from the <i>Greedy-Choice Property</i> (exchange argument proves the two least frequent nodes must be siblings at maximum depth in an optimal tree) and <i>Optimal Substructure</i> (collapsing sibling leaves into their sum-weight parent preserves optimality by mathematical induction). Coding efficiency is <b>99.28%</b> with a compression ratio of <b>1.3636 : 1</b> (<b>26.67% bandwidth savings</b>).",
        body_style
    ))

    # Section 4
    story.append(Paragraph("4. Shannon-Fano Coding & Mathematical Counterexample", h1_style))
    story.append(Paragraph(
        "Shannon-Fano recursively bipartitions sorted symbols top-down to balance subgroup probabilities. "
        "Because it makes irreversible top-down decisions, it can produce strictly suboptimal code lengths.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Mathematically Proven Counterexample:</b> Alphabet Σ = {A: 35, B: 17, C: 17, D: 16, E: 15}.<br/>"
        "• <b>Shannon-Fano:</b> Splits {A, B} (sum 52) vs {C, D, E} (sum 48). Results in codewords: A: 00 (len 2), B: 01 (len 2), C: 10 (len 2), D: 110 (len 3), E: 111 (len 3). "
        "<b>Average length = 2.3100 bits/message</b>.<br/>"
        "• <b>Huffman:</b> Bottom-up merges (15+16=31), (17+17=34), (31+34=65), (35+65=100). Codewords: A: 0 (len 1), D: 100 (len 3), E: 101 (len 3), B: 110 (len 3), C: 111 (len 3). "
        "<b>Average length = 2.3000 bits/message</b>.<br/>"
        "• <b>Suboptimality Proof:</b> L_SF - L_Huff = <b>+0.0100 bits/message (Shannon-Fano is strictly suboptimal)</b>.<br/>"
        "• <b>8-Symbol IoT Counterexample:</b> {OK: 37, TEMP_HI: 16, TEMP_LO: 16, HUM: 9, VIB: 7, DOOR: 7, FAULT: 5, RESET: 3} yields L_Huff = <b>2.6500</b> vs L_SF = <b>2.6900</b> (+0.0400 deficit).",
        body_style
    ))

    # Section 5
    story.append(Paragraph("5. Linear-Time Two-Queue Huffman Algorithm (van Leeuwen, 1976)", h1_style))
    story.append(Paragraph(
        "By maintaining two FIFO queues—Queue 1 containing pre-sorted leaf nodes and Queue 2 containing newly merged internal nodes—the "
        "Two-Queue algorithm selects the two minimum-weight nodes in O(1) time without heap adjustments. Monotonicity of Queue 2 is maintained "
        "by mathematical induction since parent weights are non-decreasing. "
        "<b>Tree construction time is strictly O(N)</b>. If sorting is included, total complexity is O(N log N) (or O(N) with counting sort). "
        "Weighted path lengths and generated code lengths are mathematically equivalent to min-heap Huffman (L = 2.2000 bits).",
        body_style
    ))

    # Section 6
    story.append(Paragraph("6. Network Bandwidth & Link Utilization Analysis", h1_style))
    story.append(Paragraph(
        "Aggregate traffic rate = 40 messages/second across 5,000 sensors. Physical capacity = 9,600 bps.",
        body_style
    ))

    net_table_data = [
        [Paragraph("Metric", table_cell_header), Paragraph("Formula", table_cell_header), Paragraph("Original (3-bit)", table_cell_header), Paragraph("Huffman (2.2-bit)", table_cell_header), Paragraph("Package-Merge (2.3-bit)", table_cell_header)],
        [Paragraph("Bitrate", table_cell_bold), Paragraph("λ × L", table_cell), Paragraph("120.00 bps", table_cell), Paragraph("88.00 bps", table_cell_bold), Paragraph("92.00 bps", table_cell_bold)],
        [Paragraph("Channel Utilization", table_cell_bold), Paragraph("Bitrate / 9600", table_cell), Paragraph("1.250 %", table_cell), Paragraph("0.917 %", table_cell_bold), Paragraph("0.958 %", table_cell_bold)],
        [Paragraph("Bandwidth Freed", table_cell_bold), Paragraph("R_orig - R_comp", table_cell), Paragraph("0.00 bps", table_cell), Paragraph("32.00 bps (26.67%)", table_cell_bold), Paragraph("28.00 bps (23.33%)", table_cell_bold)],
        [Paragraph("Bandwidth Saved / Hr", table_cell_bold), Paragraph("R_saved × 3600", table_cell), Paragraph("0 bits", table_cell), Paragraph("115,200 bits (14.4 kB)", table_cell_bold), Paragraph("100,800 bits (12.6 kB)", table_cell_bold)],
        [Paragraph("Available Headroom", table_cell_bold), Paragraph("9600 - Bitrate", table_cell), Paragraph("9,480 bps (98.75%)", table_cell), Paragraph("9,512 bps (99.08%)", table_cell_bold), Paragraph("9,508 bps (99.04%)", table_cell_bold)],
    ]
    t3 = Table(net_table_data, colWidths=[105, 95, 95, 105, 104])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t3)
    story.append(Spacer(1, 6))

    # Section 7
    story.append(Paragraph("7. Length-Limited Huffman Coding & Package-Merge Algorithm", h1_style))
    story.append(Paragraph(
        "Because ordinary Huffman produces 5-bit (`DOOR`) and 6-bit (`FAULT`, `RESET`) codewords that violate the 4-bit hardware limit, "
        "we implement the Package-Merge algorithm (Larmore & Hirschberg, 1990). The algorithm reduces the problem to an integer knapsack "
        "by iteratively packaging adjacent items and merging with base items across L_max levels.",
        body_style
    ))

    pm_table_data = [
        [Paragraph("Symbol", table_cell_header), Paragraph("Freq", table_cell_header), Paragraph("PM Codeword", table_cell_header), Paragraph("Length", table_cell_header), Paragraph("p(i) * l(i)", table_cell_header), Paragraph("Hardware Status", table_cell_header)],
        [Paragraph("OK", table_cell_bold), Paragraph("52", table_cell), Paragraph("0", table_cell_bold), Paragraph("1", table_cell), Paragraph("0.5200", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("TEMP_HI", table_cell_bold), Paragraph("14", table_cell), Paragraph("100", table_cell_bold), Paragraph("3", table_cell), Paragraph("0.4200", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("DOOR", table_cell_bold), Paragraph("4", table_cell), Paragraph("1010", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.1600", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("FAULT", table_cell_bold), Paragraph("2", table_cell), Paragraph("1011", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.0800", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("HUM", table_cell_bold), Paragraph("9", table_cell), Paragraph("1100", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.3600", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("RESET", table_cell_bold), Paragraph("1", table_cell), Paragraph("1101", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.0400", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("TEMP_LO", table_cell_bold), Paragraph("11", table_cell), Paragraph("1110", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.4400", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("VIB", table_cell_bold), Paragraph("7", table_cell), Paragraph("1111", table_cell_bold), Paragraph("4", table_cell), Paragraph("0.2800", table_cell), Paragraph("COMPLIANT (<= 4 bits)", table_cell)],
        [Paragraph("AVERAGE / TOTAL", table_cell_header), Paragraph("100", table_cell_header), Paragraph("Kraft = 1.000", table_cell_header), Paragraph("Max = 4", table_cell_header), Paragraph("L = 2.3000", table_cell_header), Paragraph("100% HARDWARE COMPATIBLE", table_cell_header)],
    ]
    t4 = Table(pm_table_data, colWidths=[80, 45, 90, 75, 80, 134])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#16a34a")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t4)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Exhaustive Brute-Force Proof:</b> Tested all 4^8 = 65,536 possible length configurations satisfying Kraft's inequality. "
        "Global minimum cost is <b>230.00 bits (2.3000 bits/message)</b>, identical to the Package-Merge output. "
        "The small 0.1000 bit/message trade-off guarantees zero register overflows in receiver firmware while delivering <b>23.33% bandwidth savings</b>.",
        body_style
    ))

    # Section 8
    story.append(Paragraph("8. Automated Test Verification & Acceptance Status", h1_style))
    story.append(Paragraph(
        "All mathematical derivations and algorithms are verified via 12 comprehensive unit and integration test suites in `backend/app/tests/`. "
        "Kraft inequality (sum 2^-l <= 1), round-trip lossless reconstruction, Two-Queue equivalence, Shannon-Fano counterexample suboptimality, "
        "and Package-Merge hardware compliance are rigorously confirmed.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_path}")

if __name__ == "__main__":
    out = "docs/MATHEMATICAL_SPECIFICATION.pdf"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    generate_pdf(out)

