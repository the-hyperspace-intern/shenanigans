def show(*args, **kwargs):
    print("UWU")
    # If we've already shown this canvas elsewhere, don't create a new one,
    # just reuse it and scroll to the existing one.
    existing = plt.get_element("")
    if existing is not None:
        plt.draw_idle()
        existing.scrollIntoView()
        return

    # Disable the right-click context menu.
    # Doesn't work in all browsers.
    def ignore(event):
        event.preventDefault()
        return False

    # Create the main canvas and determine the physical to logical pixel
    # ratio
    canvas = document.createElement("canvas")
    context = canvas.getContext("2d")
    plt._ratio = plt.get_dpi_ratio(context)

    width, height = plt.get_width_height()
    width *= plt._ratio
    height *= plt._ratio
    div = plt._create_root_element()
    add_event_listener(div, "contextmenu", ignore)
    div.setAttribute(
        "style",
        "margin: 0 auto; text-align: center;" + f"width: {width / plt._ratio}px",
    )
    div.id = plt._id

    # The top bar
    top = document.createElement("div")
    top.id = plt._id + "top"
    top.setAttribute("style", "font-weight: bold; text-align: center")
    top.textContent = plt._title
    div.appendChild(top)

    # A div containing two canvases stacked on top of one another:
    #   - The bottom for rendering matplotlib content
    #   - The top for rendering interactive elements, such as the zoom
    #     rubberband
    canvas_div = document.createElement("div")
    canvas_div.setAttribute("style", "position: relative")

    canvas.id = plt._id + "canvas"
    canvas.setAttribute("width", width)
    canvas.setAttribute("height", height)
    canvas.setAttribute(
        "style",
        "left: 0; top: 0; z-index: 0; outline: 0;"
        + "width: {}px; height: {}px".format(width / plt._ratio, height / plt._ratio),
    )
    canvas_div.appendChild(canvas)

    rubberband = document.createElement("canvas")
    rubberband.id = plt._id + "rubberband"
    rubberband.setAttribute("width", width)
    rubberband.setAttribute("height", height)
    rubberband.setAttribute(
        "style",
        "position: absolute; left: 0; top: 0; z-index: 0; "
        + "outline: 0; width: {}px; height: {}px".format(
            width / plt._ratio, height / plt._ratio
        ),
    )
    # Canvas must have a "tabindex" attr in order to receive keyboard
    # events
    rubberband.setAttribute("tabindex", "0")
    # Event handlers are added to the canvas "on top", even though most of
    # the activity happens in the canvas below.
    add_event_listener(rubberband, "mousemove", plt.onmousemove)
    add_event_listener(rubberband, "mouseup", plt.onmouseup)
    add_event_listener(rubberband, "mousedown", plt.onmousedown)
    add_event_listener(rubberband, "mouseenter", plt.onmouseenter)
    add_event_listener(rubberband, "mouseleave", plt.onmouseleave)
    add_event_listener(rubberband, "keyup", plt.onkeyup)
    add_event_listener(rubberband, "keydown", plt.onkeydown)
    context = rubberband.getContext("2d")
    context.strokeStyle = "#000000"
    context.setLineDash([2, 2])
    canvas_div.appendChild(rubberband)

    div.appendChild(canvas_div)

    # The bottom bar, with toolbar and message display
    bottom = document.createElement("div")
    toolbar = plt.toolbar.get_element()
    bottom.appendChild(toolbar)
    message = document.createElement("div")
    message.id = plt._id + "message"
    message.setAttribute("style", "min-height: 1.5em")
    bottom.appendChild(message)
    div.appendChild(bottom)

    plt.draw()
