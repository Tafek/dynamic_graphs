Ich abuse diesen Part erstmal als eine Anleitung für mich, was ich tun will und was getan werden muss:

Ich würde gerne einen Code schreiben, bei dam man ein beliebiges Dataset als CSV (ggf später auch mit DB-Input als Erweiterung?) an den Code übergeben kann.
Dieser Code liest dann die Spalten Aus und bietet anhand derer dann die Möglichkeit:
1. Sich verschiedene Visualisierungsstyles ausgeben zu lassen (Barchart, Scatter, Linegraph, Piechart)
2. Sich verschiedene Spalten anzeigen zu lassen.
3. Verschiedene Filter anzuwenden.

Die Reihenfolge des Codes müsste also grob wie folgt sein:
1. User gibt den Input in Form einer CSV (später ggf auch in Form einer DB die gequeried wird)
    -> Das müsste vermutlich Codeseitig in CSV sein, wo man die Datei (und später Query + Credentials) an entsprechender Stelle ablegt.
    -> Potentiell könnte man es natürlich auch über einen Upload/Input im Interface machen, aber da bin ich mir unsicher ob ich den Upload packe.

2. Der Input müsste durch die erste Funktion laufen, die dem Interface die Spalten überreicht.
    -> Gut wäre hier auch schon eine Bereinigung / Erkennung, was für Spalten vorliegen, auch wenn der Typus ggf nicht stimmt.
        -> Spalten mit nur "Ja/Nein" ("Yes"/"No") sollten z.B. als Kategorisch behandelt werden. (Ebenso mit nur wenigen verschiedenen Strings), etc.

3. Der Input der Funktion aus 2. fließt zurück ins Interface und bietet basierend darauf einen Spalten Selector. Der User kann entsprechend X verschiedene Spalten für seine Visualisierung aus- und abwählen.

4. Die Auswahl aus 3. (die auch einen Visualisierungstypen umfasst) muss zu einem Visual führen.
    -> Via Switch Case (oder einer if-Schleife) wird nach Visualisierungstypen ausgewählt und basierend darauf die entsprechenden Spalten visualisiert.
    -> Passend wäre hierbei noch filter zu erlauben, sodass ich z.B. nur bestimmte Werte Spalten auswählen kann, die Range des Datums bestimmen kann, etc.
        -> Faktisch alles, was ich mir ggf. händisch anpassen wollen würde.

5. Auch die Visualisierung soll ggf angepasst werden können. (Xlim/Ylim/Ticks/etc.)
6. Fehlermeldungen / Warnhinweise sollten geworfen werden (z.B. mehrere Spalten in einem Pie-Chart.)



Echte Readme, grob skiziiert:

1. Installationsprozess Yadda-Yadda
2. Im VSC-Terminal "uv run python main.py" ausführen.
    -> Es gibt entsprechend einen Return à la "Running on http://127.0.0.1:5000" -> Diese IP über die URL-Zeile des Browsers aufrufen.