from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class ToDoApp(App):
    def build(self):
        self.tasks = []

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10) 

        # Input field for new tasks
        self.task_input = TextInput(hint_text='Enter a task', size_hint_y=None, height=50)
        layout.add_widget(self.task_input)

        # Button to add tasks 
        add_button = Button(text='Add Task', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_task)
        layout.add_widget(add_button)

        # Scrollable area for tasks
        self.task_list = GridLayout(cols=1, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.task_list)
        layout.add_widget(scroll_view)

        return layout
    
    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:
            task_label = Label(text=task_text, size_hint_y=None, height=40)
            self.task_list.add_widget(task_label)
            self.tasks.append(task_text)
            self.task_input.text = ''

if __name__ == '__main__':
    ToDoApp().run()
            