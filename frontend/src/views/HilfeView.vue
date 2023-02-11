<template>
  <v-container class="px-10 py-0 main-container">
    <v-col cols="12" class="d-flex flex-row px-0" style="align-items: center">
      <h1>Hilfe</h1>
    </v-col>
    <v-divider></v-divider>
    <v-row class="mt-2" style="min-height: 450px">
      <v-col>
        <h2>Allgemeines</h2>
        <p>Auf <a href="https://drv-stats.up.railway.app/">https://drv-stats.up.railway.app/</a> können automatisiert
          erfasste öffentlich zugängliche Wettkampf- und Ergebnisdaten (EM, WM, OS) anhand verschiedener Filterkriterien
          abgerufen werden. Hierzu stehen sechs Module zur Verfügung:</p>
        <br>
        <h3>Kalender</h3>
        <p>In diesem Modul sind die erfassten Wettkämpfe in einer übersichtlichen Kalenderansicht aufgeführt. Per Klick
          auf einen Wettkampf gelangt man direkt zu den aufbereiteten Ergebnissen.</p>
        <br>
        <h3>Berichte</h3>
        <p>In diesem Modul können spezifische Übersichten zu Fahrzeiten im Quer- und Längsschnitt anhand diverser
        Filterkriterien erstellt und abgerufen werden.</p>
        <br>
        <h3>Rennstrukturanalyse</h3>
        <p>In diesem Modul werden die zur Verfügung stehenden 500m Abschnittszeiten sowie GPS-Daten (50m Auflösung) im
        Rennverlauf tabellarisch und grafisch aufbereitet.</p>
        <br>
        <h3>Athleten</h3>
        <p>In diesem Modul können Stammdaten wie z.B. Disziplin und Medaillenstatistiken sowie eine Auflistung von
        Wettkampfergebnissen einzelner Athleten abgerufen werden.</p>
        <br>
        <h3>Teams</h3>
        <p>In diesem Modul können Übersichten bezüglich der Bootsbesetzungen einer Nation im Rahmen eines bestimmten
        Wettkampfes abgerufen werden.</p>
        <br>
        <h3>Medaillenspiegel</h3>
        <p>In diesem Modul können spezifische Übersichten zu Platzierungen und Medaillenspiegeln im Quer- und Längsschnitt
        abgerufen werden.</p>
        <br>
        <p>Alle Module sind prinzipiell gleich aufgebaut. In der linken oberen Bildschirmseite findest du unter dem
        „Filtersymbol“ das Filtermenü. Durch Auswahl entsprechender Filterkriterien kann die Datenabfrage mit
        zunehmender Anzahl der genutzten Kriterien spezifiziert werden. Über den Button „Übernehmen“ kann die Auswahl
        bestätigt werden und die entsprechenden Daten werden anhand von Tabellen sowie interaktiven Grafiken ausgegeben.
        Über das Symbol <v-icon color="grey" class="v-icon--size-medium">mdi-table-arrow-right</v-icon> können die Daten dann im csv Format für die weitere private Verwendung abgerufen werden.</p>

      </v-col>
      <v-col cols="1">

      </v-col>
      <v-col>
        <h2>Abkürzungsverzeichnis</h2>
        <h3><i>Bootsklasse</i></h3>

        <table>
          <tr v-for="abbreviation, key in abbreviations">
            <template v-if="abbreviation === null">
              <th>&nbsp;</th>
              <td></td>
            </template>
            <template v-else>
              <th>{{ key }}</th>
              <td>{{ abbreviation }}</td>
            </template>
          </tr>
        </table>

      </v-col>
    </v-row>


  </v-container>
</template>

<script>
export default {
  data() {
    return {
      abbreviations: {
        "JM1x": "Junior Men's Single Sculls/U19 Männer-Einer",
        "JM2x": "Junior Men's Double Sculls/U19 Männer-Doppelzweier",
        "JM4x": "Junior Men's Quadruple Sculls/U19 Männer-Doppelvierer",
        "JM2-": "Junior Men's Pair/U19 Männer-Zweier",
        "JM4+": "Junior Men's Coxed Four/U19 Männer-Vierer mit Steuermann:frau",
        "JM4-": "Junior Men's Four/U19 Männer-Vierer",
        "JM8+": "Junior Men's Eight/U19 Männer-Achter mit Steuermann:frau",
        "space": null,
        "JW1x": "Junior Women's Single Sculls/U19 Frauen-Einer",
        "JW2x": "Junior Women's Double Sculls/U19 Frauen-Doppelzweier",
        "JW4x": "Junior Women's Quadruple Sculls/U19 Frauen-Doppelvierer",
        "JW2-": "Junior Women's Pair/U19 Frauen-Zweier",
        "JW4+": "Junior Women's Coxed Four/U19 Frauen-Vierer mit Steuermann:frau",
        "JW4-": "Junior Women's Four/U19 Frauen-Vierer",
        "JW8+": "Junior Women's Eight/U19 Frauen-Achter mit Steuermann:frau",
        "space1": null,
        "BM1x": "U23 Men's Single Sculls/U23 Männer-Einer",
        "BM2x": "U23 Men's Double Sculls/U23 Männer-Doppelzweier",
        "BM4x": "U23 Men's Quadruple Sculls/U23 Männer-Doppelvierer",
        "BM2-": "U23 Men's Pair/U23 Männer-Zweier",
        "BM4+": "U23 Men's Coxed Four/U23 Männer-Doppelvierer",
        "BM4-": "U23 Men's Four/U23 Männer-Vierer",
        "BM8+": "U23 Men's Eight/U23 Männer-Achter mit Steuermann:frau",
        "BLM1x": "U23 Lightweight Men's Single Sculls/U23 Leichtgewichts-Männer-Einer",
        "BLM2x": "U23 Lightweight Men's Double Sculls/U23 Leichtgewichts-Männer-Doppelzweier",
        "BLM4x": "U23 Lightweight Men's Quadruple Sculls/U23 Leichtgewichts-Männer-Doppelvierer",
        "BLM2-": "U23 Lightweight Men's Pair/U23 Leichtgewichts-Männer-Zweier",
        "space2": null,
        "BW1x": "U23 Women's Single Sculls/U23 Frauen-Doppelzweier",
        "BW2x": "U23 Women's Double Sculls/U23 Frauen-Doppelvierer",
        "BW4x": "U23 Women's Double Sculls/U23 Frauen-Doppelvierer",
        "BW2-": "U23 Women's Quadruple Sculls/U23 Frauen-Zweier",
        "BW4-": "",
        "BW4+": "",
        "BW8+": "",
        "BLW1x": "",
        "BLW2x": "",
        "BLW4x": "",
        "BLW2-": "",




      },
    }
  }
}

</script>

<style lang="scss" scoped>
th {
  text-align: left;
  padding-right: 50px;
}
</style>


U23 Women's Pair/ U23 Frauen-Doppelvierer
U23 Women's Four/U23 Frauen-Vierer
Under 23 Women's Coxed Four/U23 Frauen-Vierer
U23 Women's Eight/U23 Frauen-Achter mit Steuermann:frau
U23 Lightweight Women's Single Sculls/U23 Leichtgewichts-Frauen-Einer
U23 Lightweight Women's Double Sculls/U23 Leichtgewichts-Frauen-Doppelzweier
U23 Lightweight Women's Quadruple Sculls/U23 Leichtgewichts-Frauen-Doppelvierer
Under 23 Lightweight Women's Pair/U23 Leichtgewichts-Frauen-Zweier
	
M1x	    Men's Single Sculls/Männer-Einer
M2x	    Men's Double Sculls/Männer-Doppelzweier
M4x	    Men's Quadruple Sculls/Männer-Doppelvierer
M2-	    Men's Pair/Männer-Zweier
M4-	    Men's Four/Männer-Vierer
M8+	    Men's Eight/Männer-Achter mit Steuermann:frau
LM1x	  Lightweight Men's Single Sculls/Leichtgewichts-Männer-Einer
LM2x	  Lightweight Men's Double Sculls/Leichtgewichts-Männer-Doppelzweier
LM4x	  Lightweight Men's Quadruple Sculls/Leichtgewichts-Männer-Doppelvierer
LM2-	  Lightweight Men's Pair/Leichtgewichts-Männer-Zweier
	
W1x	Women's Single Sculls/Frauen-Einer
W2x	Women's Double Sculls/Frauen-Doppelzweier
W4x	Women's Quadruple Sculls/Frauen-Doppelvierer
W2-	Women's Pair/Frauen-Zweier
W4-	Women's Four/Frauen-Vierer
W8+	Women's Eight/Frauen-Achter mit Steuermann:frau
LW1x	Lightweight Women's Single Sculls/ Leichtgewichts-Frauen-Einer
LW2x	Lightweight Women's Double Sculls/ Leichtgewichts-Frauen-Doppelzweier
LW4x	Lightweight Women's Quadruple Sculls/ Leichtgewichts-Frauen-Doppelvierer
LW2-	Lightweight Women's Pair/ Leichtgewichts-Fauen-Zweier

PR1	arms & shoulders/Arme und Schultern
PR2	trunk & arms/Oberkörper und Arme
PR3	legs, trunk & arms/Beine, Oberkörper und Arme

PR1 M1x	PR1 Men's Single Sculls/Männer-Festsitz-Einer
PR2 M1x	PR2 Men's Single Sculls/Männer-Festsitz-Einer
PR3 M2-	PR3 Men's Pair/Männer-Riemen-Zweier
	
PR1 W1x	PR1 Women's Single Sculls/Frauen-Festsitz-Einer
PR2 W1x	PR2 Women's Single Sculls/Frauen-Festsitz-Einer
PR3 W2-	PR3 Women's Pair/Frauen-Riemen-Zweier
	
PR2 Mix2x	PR2 Mixed Double Sculls/Mixed-Doppel-Zweier
PR3 Mix2x	PR3 Mixed Double Sculls/Mixed-Doppel-Zweier
PR3 Mix4+	PR3 Mixed Coxed Four/Mixed-Vierer mit Steuermann:frau
