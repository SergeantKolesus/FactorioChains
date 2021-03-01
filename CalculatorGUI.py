from appJar import gui


def CreateApp(base):
    app = gui("Calculator", "640x480")
    countInfo = "Total amount of recipeces parsed " + str(base.RecipesCount())
    app.addLabel("l1", countInfo)

    return app
