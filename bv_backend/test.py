import sys
import threading


from soma.qt_gui.test.test import TestControls


def qt_loop(controller):
    from soma.qt_gui.qt_backend import Qt
    from soma.qt_gui.controller import ControllerWidget

    app = Qt.QApplication(sys.argv)
    widget = ControllerWidget(controller)
    widget.show()
    app.exec_()

def web_loop(controller):
    import uvicorn
    from .routers.controller import published_controllers
    from .main import app
    
    global published_controllers
    published_controllers['test'] = controller
    uvicorn.run(app, host='127.0.0.1', port=8000)

if __name__ == "__main__":

    # Create the controller we want to parametrized
    controller = TestControls()

    # Set some values to the controller parameters
    controller.s = 'a text value'
    controller.n = 10.2

    controller.lls= [[],['a', 'b', 'c'],[]]

    thread = threading.Thread(target=web_loop, args=(controller,))
    thread.daemon = True
    thread.start()

    qt_loop(controller)
