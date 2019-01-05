# amnesia

I like to take notes on things. I feel like it helps me remember better, and I'm pretty forgetful anyway. I didn't really like any of the note taking / journaling programs I could easily find, so I did the obnoxious programmer thing and I'm going to make my own.

## Requirements

### 1. Domains for Notes

I work for a corporation, and as such, notes on meetings/products of that corp need to stay with them when I leave--so my note management program needs to allow for different domains, e.g. work/personal.

### 2. Simple files

I intend to use `git` to version and redundant-ify my notes, and git works best with plain text files, so I'm going to stick to those. As an added bonus, that'll let me leverage pandoc to output my notes however I want.

Using plain text will also greatly increase the flexibility of what editor I can use.

## Planned features

### 1. Templating

### 2. tags & catagory searching

### 3. managed outputting

## current to-do
- [ ] reconsider how we serialize out objects--maybe just use a simple config file (or command line args) and `pickle`, eh?