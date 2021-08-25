from typing import List, Optional

from information_extraction.Font import Font
from information_extraction.Segment import Segment
from information_extraction.SegmentTag import SegmentTag
from pdfalto.PDFFeatures import PDFFeatures
from pdfalto.PdfAltoXml import PdfAltoXml


class InformationExtraction:
    def __init__(self, xml_tags, xml_file_path: str = ''):
        self.xml_file_path = xml_file_path
        self.xml_tags = xml_tags
        self.segments: List[Segment] = list()
        self.fonts: List[Font] = list()
        self.pdf_features: Optional[PDFFeatures] = None
        self.set_segments()

    def set_segments(self):
        segments_pdfalto, fonts, self.pdf_features = PdfAltoXml(self.xml_tags).get_segments()
        self.fonts = Font.from_page_xml_tag(fonts)

        for segment_pdfalto in segments_pdfalto:
            page_width = segment_pdfalto.page_width
            page_height = segment_pdfalto.page_height
            tags = [SegmentTag(xml_tag, page_width, page_height, segment_pdfalto.page_number, self.fonts) for
                    xml_tag in
                    segment_pdfalto.xml_tags]
            if len(tags) == 0 or ''.join([x.text for x in tags]).strip() == '':
                continue

            segment = Segment(tags, self.pdf_features, segment_pdfalto.page_number)
            self.segments.append(segment)

    @staticmethod
    def from_file_content(file_content):
        xml_tags = PdfAltoXml.get_xml_tags_from_file_content(file_content)
        return InformationExtraction(xml_tags=xml_tags)

    @staticmethod
    def from_pdf_path(pdf_path: str, xml_file_path: str, failed_pdf_path:str):
        xml_tags = PdfAltoXml.from_pdf_path(pdf_path, xml_file_path, failed_pdf_path)
        if not xml_tags:
            return None
        return InformationExtraction(xml_tags=xml_tags)
