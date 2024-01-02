from tkinter import *
from deadline import *
import xml.etree.ElementTree as ET
import customtkinter
import random
import string

#     ____       ____            ____      
#    / __ \___  / __/___ ___  __/ / /______
#   / / / / _ \/ /_/ __ `/ / / / / __/ ___/
#  / /_/ /  __/ __/ /_/ / /_/ / / /_(__  ) 
# /_____/\___/_/  \__,_/\__,_/_/\__/____/  
                                         

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
root = customtkinter.CTk()
root.geometry('800x600')

deadline_list = [
    Deadline(
        label=f"Task {i + 1}",
        time=f"{random.randint(1, 12)}:{random.choice(['00', '15', '30', '45'])} {random.choice(['AM', 'PM'])} - {random.randint(1, 12)}:{random.choice(['00', '15', '30', '45'])} {random.choice(['AM', 'PM'])}",
        description=''.join(random.choices(string.ascii_letters, k=random.randint(10, 50))),
        priority=random.choice(['low', 'medium', 'high']),
        status=random.choice(['pending', 'in progress', 'completed']),
        project=f"Project {random.randint(1, 5)}",
        attachments=[f"file_{j}.docx" for j in range(random.randint(0, 3))]
    )
    for i in range(5)
]


#    _  __ __  _____       ____  ____  __________  ___  ______________  _   _______
#   | |/ //  |/  / /      / __ \/ __ \/ ____/ __ \/   |/_  __/  _/ __ \/ | / / ___/
#   |   // /|_/ / /      / / / / /_/ / __/ / /_/ / /| | / /  / // / / /  |/ /\__ \ 
#  /   |/ /  / / /___   / /_/ / ____/ /___/ _, _/ ___ |/ / _/ // /_/ / /|  /___/ / 
# /_/|_/_/  /_/_____/   \____/_/   /_____/_/ |_/_/  |_/_/ /___/\____/_/ |_//____/  
                                                                                

xml_root = ET.Element("Tasks")
for i, deadline in enumerate(deadline_list):
    xml_root.append(deadline.to_xml_element())

tree = ET.ElementTree(xml_root)
tree.write("tasks.xml", encoding="utf-8", xml_declaration=True)

loaded_deadlines = []
tree = ET.parse("tasks.xml")
xml_root = tree.getroot()


for i, deadline_element in enumerate(xml_root.findall("Deadline")):
    loaded_deadlines.append(Deadline.from_xml_element(deadline_element))

    # Frame for each task
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(side='top', fill='x', padx=10, pady=5, ipadx=10, ipady=5)

    # Task Label
    task_label = customtkinter.CTkLabel(master=frame, text=loaded_deadlines[i].display_task(), fg_color="transparent")
    task_label.pack(side='left')

    # Priority Label
    priority_label = customtkinter.CTkLabel(master=frame, text=f"Priority: {loaded_deadlines[i].priority}", fg_color="transparent")
    priority_label.pack(side='right')

root.mainloop()
