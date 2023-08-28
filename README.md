# General
Dieses Script kann zum automatischen Senden von E-Mails verwendet werden.

Kann unter aderem hilfreich sein um Sponsoren für Erstie-Tüten anzuschreiben.

# Ausführen

Zuerst die env-vars `hsma_username` und `hsma_password` exportieren.

In Config.py die felder ausfüllen oder ausgefüllt lassen und beispiel-dateien beschreiben.
Das Anschreiben kommt in anschreiben_example.txt
Die Felder die Ersetzt werden sollen kommen in rec_example.csv

Alle Felder die im Mailtext jeweils mit einem Underscore vorne und hinten versehen sind und für die ein Feld in rec-example.csv existiert, werden ersetzt.