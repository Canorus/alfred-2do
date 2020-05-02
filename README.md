# alfred-2do

Also check out different workflow [made by hylo](https://github.com/hylo926/alfred-2do).

------

Mimic natural language detection when creating a 2Do task.

USAGE:

```
2d event [on|at|by|from] [dd/MM/YY|mm:hh[pm]] [near [location]] [@[list]] [#[tag]] [[*][**][***]] [-web] [-proj|-check]
```

On 2.0 workflow will try to detect date format(dd/MM/YY) of time format(mm:hh) after keyword `on` `at` `by` or  `from`. If these keywords are not followed by date format or time format, it will be included back to event name. Keyword `by` only sets due date/time and keyword `from` only sets start date/time. 

Keep in my there's no space between time and `pm` keyword in time format.

Location after `near` keyword sets location. Requires location be set beforehand.

List can be designated with `@` sign. No space between `@` sign and list name.

Multiple hashtags can be attached.

Importance can be applied with 1~3 of asterisks.

\+ ~~This workflow will automatically detect and add webpage url currently you're watching as an action to open the webpage.~~ You can choose whether or not to add web page or not by adding `-web` flag. **Only works with Safari and Chrome. Does not work with Firefox browser.** [why](https://github.com/Canorus/alfred-2do/issues/3)

Event type can also be `project` or `checklist`. Apply with keyword `-proj` or `-check`.

~~caveat: It takes bit of time for this script to dissect your input and understand your intention. So it is recommended you **pause 1 second before pressing return key** to create a new task. I'm looking for ways to solve this issue.~~ Solved by v 1.1

------

Many thanks to Fahad G. for providing icons :D Black icons are also included in case you're using light alfred theme. All the icons are edited based on original icon provided.

Also big shout out to [@doomsheart](https://github.com/doomsheart) reviewing the whole code for me.

Massive shout out to [@hylo](https://github.com/hylo926) for contribution. Check out his workflow [here](https://github.com/hylo926/alfred-2do)

based on the work of [2Do Workflow by Caleb Grove](https://www.alfredforum.com/topic/3811-2do-workflow/?do=findComment&comment=22721)

webpage detection code from [fallroot's copy-url-for-alfred](https://github.com/fallroot/copy-url-for-alfred)

[you can try at your own risk](https://github.com/Canorus/alfred-2do/raw/master/workflow/alfred-2Do_2.0.alfredworkflow) and any suggestions/pull requests will be appreciated

- [x] ~~only single tag is accepted; working on it~~
- [x] ~~priority~~
