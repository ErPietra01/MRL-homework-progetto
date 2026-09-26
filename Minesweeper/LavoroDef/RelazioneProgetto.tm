<TeXmacs|2.1.4>

<style|<tuple|generic|italian>>

<\body>
  <doc-data|<doc-title|Sviluppo di un agente che apprenda il gioco
  Minesweeper tramite Reinforcement Learning>|<doc-author|<author-data|<author-name|Ettore
  Pietrabissa e Sara Travaglini>|<\author-affiliation>
    Progetto del corso di Machine and Reinforcement Learning for Control
    Applications

    Prof. Corrado Possieri

    A.A. 2025/2026
  </author-affiliation>>>>

  <section|Introduzione>

  Il progetto scelto consiste nello sviluppare un agente in grado di
  apprendere le regole del gioco Campo Minato (Minesweeper) in modo tale da
  vincere. Lo sviluppo dell'agente ha comportato numerose complicazioni
  legate alla complessità del caso di studio, in particolare lo studio degli
  stati e l'analisi dell'ambiente utilizzato.

  L'ambiente è disponibile nella repository:
  https://github.com/sdlee94/Minesweeper-AI-Reinforcement-Learning.

  La prima difficoltà ha riguardato il fatto che, per risolvere il campo
  minato, è opportuno implementare una rete neurale profonda

  <section|L'algoritmo Expected SARSA>

  Il progetto è stato svolto tramite l'implementazione di Expected SARSA

  \;

  NOTE: con diminishing epsilon e un tabellone piu piccolo, il plateau è
  ancora presente ma per valori più prossimi a zero e oscilla di meno
</body>

<\initial>
  <\collection>
    <associate|page-medium|paper>
  </collection>
</initial>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|?|../../../../.TeXmacs/texts/scratch/no_name_1.tm>>
    <associate|auto-2|<tuple|2|?|../../../../.TeXmacs/texts/scratch/no_name_1.tm>>
  </collection>
</references>