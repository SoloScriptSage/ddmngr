import xml.etree.ElementTree as ET

class Deadline:
    def __init__(self, label, time, description="", priority=0, status="pending", project="", attachments=None):
        self.label = label
        self.time = time
        self.description = description
        self.priority = priority
        self.status = status
        self.project = project
        self.attachments = attachments or []

    def display_task(self):
        return f"Label: {self.label}\nTime: {self.time}\nDescription: {self.description}\nPriority: +{self.priority}\nStatus: {self.status}\nProject: {self.project}\nAttachments: {', '.join(self.attachments)}"

    def to_xml_element(self):
        task_element = ET.Element("Deadline")
        ET.SubElement(task_element, "Label").text = self.label
        ET.SubElement(task_element, "Time").text = self.time
        ET.SubElement(task_element, "Description").text = self.description
        ET.SubElement(task_element, "Priority").text = str(self.priority)
        ET.SubElement(task_element, "Status").text = self.status
        ET.SubElement(task_element, "Project").text = self.project

        attachments_element = ET.SubElement(task_element, "Attachments")
        for attachment in self.attachments:
            ET.SubElement(attachments_element, "Attachment").text = attachment

        return task_element

    def to_xml_string(self):
        task_element = self.to_xml_element()
        return ET.tostring(task_element, encoding='unicode')

    @classmethod
    def from_xml_element(cls, xml_element):
        label = xml_element.find("Label").text
        time = xml_element.find("Time").text
        description = xml_element.find("Description").text
        priority_text = xml_element.find("Priority").text
        priority = cls.parse_priority(priority_text)  # Use a method to handle non-numeric priority
        status = xml_element.find("Status").text
        project = xml_element.find("Project").text

        attachments_element = xml_element.find("Attachments")
        attachments = [attachment.text for attachment in attachments_element.findall("Attachment")]

        return cls(label=label, time=time, description=description, priority=priority, status=status, project=project, attachments=attachments)

    @classmethod
    def from_xml_string(cls, xml_string):
        xml_element = ET.fromstring(xml_string)
        return cls.from_xml_element(xml_element)

    def parse_priority(priority_text):
        try:
            return int(priority_text)
        except ValueError:
            # Handle non-numeric priorities, for example: 'low', 'medium', 'high'
            priority_text_lower = priority_text.lower()
            if priority_text_lower == 'low':
                return 1
            elif priority_text_lower == 'medium':
                return 2
            elif priority_text_lower == 'high':
                return 3
            else:
                # Default to 0 or any other appropriate value
                return 0
