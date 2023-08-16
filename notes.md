modularize the code a bit -- make smaller so llm can handle smaller parts. have it do the separation, give enough instruction
new commands, like /fix-quarto or /fix-python that diagnosis the issue
next step is finally langchain and adding memory? use html > md method to throw in docs? will that suffice? if not, command for like /summarize or something that does something special idk
CLI should contain "magic" commands. w/ move to langchain, bust those out into separate commands and "icode" w/ slash commands for all of them because the way. 
see if typer supports auto-fast api. if so, see if fastapi works on streamlit like magic. if so, deploy there ??? profit
/write-blog "Use the conext blah blah blah"/write-python "Use the context blah blah blah"
note these can be iterative loops. start relying on langchain/logic for flow, get used to it. build, expand, reduce, reuse, recycle 

- Cody
