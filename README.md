![Wet sand ribbed by the last wash with a thin mirror of sky in each hollow, two flags with cloth out flat, an empty lifeguard chair between them with the rescue can across its seat, breakers in white lines left and right, the calm lane running out to a shadow blue horizon, foam flecks moving seaward down its centre, and gulls standing well back on dry sand facing inland, with no lettering anywhere](intro-banner.png)

# codeintel-Dependency-Confusion-Checker

Title block: the name above is set in Battambang in shadow blue on a pale panel ruled like a beach notice board. The single warning flag below is the header plate for this repo, spent once only here. Headings after this stay typographic, shaped like depth markers on a sounding line.

![One warning flag on its pole at the waterline, cloth held out flat in deep green passing to kelp amber with shadow blue in the folds and one abalone flash on the hem, the pale calm lane behind it between breaking surf, and the name lettered below in sounding line drops, each word a measured interval below the last](logo.png)

![The beach wide at lengthening light: breakers in white lines left and right, the calm glassy lane down the middle with foam flecks drifting seaward, two warning flags at the near corners of the lane, the lifeguard high on a timber chair between them with a rescue can across the knees and a board by the chair leg, and the name painted only on the chair crossboard in kelp amber on shadow blue](banner.png)

![The beach in three depths: breaker lines arriving and spending themselves while the lane stays flat, two flags lifting, holding, and slackening in gusts, the lifeguard head turning slowly between the lane and the bathing water, and the wash withdrawing at the lower edge carrying foam flecks a short way seaward](scene.svg)


Identifies potential dependency confusion attacks by checking for inconsistencies between locally installed packages and those available in public repositories. - Focused on Tools for static code analysis, vulnerability scanning, and code quality assurance

Every run prints a closing summary with checked, failed, and not found counts. The run exits 1 when any check failed or no package could be listed at all. The line saying no potential vulnerabilities were found is printed only for a run whose checks completed. In single package mode (-p), the named package is looked up in the installed set and flagged on the same rule as a full run. Packages absent from the public index are printed as a named result class, Packages not found on the public index, not only as a log line.

> **Patrol note chalked on the tally slate: read all three counts together.** Packages the index did not answer for are counted separately as not found, under the heading Packages not found on the public index, and that class is a different kind of fact from a local version that has outrun the public one. Exit 1 has three different causes: a potential confusion found, a check failed, or nothing checked at all.


![Major separator: a column of bubbles rising and wobbling at the top, kelp amber and shadow blue on deep green](sep-heavy.svg)

## Install
`git clone https://github.com/ShadowGuardAI/codeintel-dependency-confusion-checker`

> **Patrol note chalked on the tally slate: clone line flagged.** The install line above reads git clone https://github.com/ShadowGuardAI/codeintel-dependency-confusion-checker. The organisation name in it omits the hyphen; the organisation is ShadowGuard-AI. The line is preserved as printed and flagged here, not corrected inside it.


![Minor separator: a column of bubbles rising and wobbling at the top, kelp amber and shadow blue on deep green](sep-light.svg)

## Usage
`./codeintel-dependency-confusion-checker [params]`

> **Patrol note chalked on the tally slate: usage line flagged.** The usage line above is a placeholder. No file of that name is the entry point, and the bracketed word is not an argument the program knows. The parser form is shown on the website, marked as taken from the code.


![Major separator: a column of bubbles rising and wobbling at the top, kelp amber and shadow blue on deep green](sep-heavy.svg)

## Parameters
- `-h`: Show help message and exit
- `-p`: The name of the package to check (e.g., 
- `-r`: No description provided
- `-v`: Enable verbose output for debugging.


![Minor separator: a column of bubbles rising and wobbling at the top, kelp amber and shadow blue on deep green](sep-light.svg)

> **Patrol note chalked on the tally slate: parameter gaps kept as gaps.** The entry for -p breaks off in mid phrase at the words (e.g., with nothing after them, and the entry for -r reads only No description provided. The long forms and the parser descriptions live on the website, marked as facts of the code, and are not folded into the lines above.

## License
Copyright (c) ShadowGuardAI

> **Patrol note chalked on the tally slate: closing line flagged.** The closing line above reads Copyright (c) ShadowGuardAI, the same unhyphenated fault as the clone line. The repository LICENSE file carries the MIT License. Both facts stand as printed.
