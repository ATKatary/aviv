# Usage instructions
## Minecraft vampirez minigame
Vampirez minigame is a MC mingame where players are randomly assigned a vampire or survivor role.<br>
The objective of vampires is to kill the survivors (after which they turn to vampires).<br>
The objective of survivors is to survive 20 waves (nights)<br>

### Commands 
`/vampire create <name>` - creates a new game `<name>`<br><br>
`/vampire join <name>` - joins a new game `<name>`<br><br>
`/vampire ai <reaction> <role>` - generates an ai response with `<reaction>` and `<role>` <br>

### Starting server 
To start the MC server execute the following 
````
cd ~/aviv/server 
./start
````

## Admin Panel 
The admin panel allows fine-grained control over AI prompt generation
<br>It is composed of the following models 

### Configuration
#### Fields
- `default_role`
    The default role to be used in prompt generation when no role is specified by the API request<br>

- `default_reaction`
    The default reaction to be used in prompt generation when no role is specified by the API request<br>

- `context`
    This is a string to be included with every prompt. Can include game rules, etc<br>

- `past_events_size`
    indicates how many events to consider when generating prompts<br>

- `include_prev_conv`
    flag for including the past conversation or not<br>

- `prompt`
    the prompt to use for generating the response<br>

### Role
- `name`
    a 26 max character identifier for the role (must be unique)<br>

- `objective`
    a string detailing what the role is / does<br>

### Reaction
#### Fields
- `name`
    a 26 max character identifier for the reaction (must be unique)<br>

### Prompt
#### Fields
- `name`
    a 50 max character identifier for the prompt (must be unique)<br>

- `format`
    a list of strings elements, where every element is a piece of the prompt<br>
    each element can be text of a variable<br>
    variables are demarked by a `!` before the variable name<br>
    #### example 
    prompt: "Generate a !reaction.name response based on the past !config.past_events_size from the following !past_events"<br>
    format: [
    *   "Generate a",<br>
        "!reaction.name",<br>
        "response based on the past",<br>
        "!config.past_events_size",<br>
        "from the following",<br>
        "!past_events"<br>

    ]<br><br>

    The possible prompt variables are:
    - `role.name`
    - `role.objective`
    - `reaction.name`
    - `past_events`
    - `config.context`
    - `config.past_events_size`
    <br><br>

    Notice that past_events is the only variable without a model. This is because it is also a generated variable<br>

    The `past_events` is created by finding all recorded `Event` models and formatting them according to the `EventFormat` specified for each event's type<br>
   
    See `EventFormat` for more info<br>

### Event
#### Fields
- `cash`
    how much cash the player has<br>

- `wave`
    which wave it is currently<br>

- `is_vampire`
    falg for whether player is a vampire<br>

- `is_survivor`
    falg for whether player is a survivor<br><br>

- `inventory`
    a list of items in the player's inventory when the event was recorded<br>

- `user`
    the user we are recording event for<br>

- `team`
    a list of users that are on the player's team (vampires or survivors)<br>

- `trigger_time`
    the time this event recording was triggered<br>

- `trigger`
    the name of the trigger that initiated the recording of this event<br>
    Every trigger has a corresponding `EventFormat` that is used to format the event when generating the `past_events` variable

### EventFormat
- `name`
    the name of the trigger for which this formatter is to be used<br>

- `format`
    a list of strings elements, where every element is a piece of the prompt<br>
    each element can be text of a variable<br>
    variables are demarked by a `!` before the variable name<br>
    #### example 
    event format: "!event.user has !event.cash on him right now and the following items: !event.inventory"<br>
    format: [<br>
    *  "!event.user",<br>
        "has",<br>
        "!event.cash",<br>
        "on him right now and the following items:",<br>
        "!event.inventory"<br>

    ]<br><br>

    The possible event variables are:
    - `event.cash`
    - `event.wave`
    - `event.winner`
    - `event.is_vampire`
    - `event.is_survivor`
    - `event.inventory`
    - `event.user`
    - `event.team`
    - `event.trigger`
    - `event.trigger_time`
    <br><br>

#### Notes
Whenever you are creating a format a space is added by default between each element, so there is no need to worry about spaces between elements.<br>
**Example 1:**<br>
- format: [
    *   "Generate a",<br>
        "!reaction.name"<br>
]
- prompt: "Generate a !reaction.name

**Example 1:**<br>
- format: [
    *   "Generate a ",<br>
        "!reaction.name"<br>
]
- prompt: "Generate a  !reaction.name"
