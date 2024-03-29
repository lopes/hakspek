# Hakspek
A SEO Advisor for my blog posts using OpenAI's ChatGPT.  This project is based on similar ones I found in the web, like [this](https://medium.com/geekculture/a-paper-summarizer-with-python-and-gpt-3-2c718bc3bc88).

It was designed to be used as a SEO advisor for my blog posts that are written in Markdown format with a [Zola](https://www.getzola.org/) header, but it can also be used as a module.

**Hakspek** is defined by the [The New Hacker's Dictionary](https://mitpress.mit.edu/9780262680929/the-new-hackers-dictionary/) as *a shorthand method of spelling found on many British academic bulletin boards and talker systems*.  I chose it because this project is meant to simplify my writing process.


## Usage
Assuming the files to be processed are in `~/texts` and you're under `$HOME`, first clone this repository, navigate inside it, and install the required modules:

```sh
git clone https://github.com/lopes/hakspek
cd hakspek
python3 -m venv venv
pip install -r requirements.txt
```

Now, you can process the whole directory (including subdirectories) of texts at once or you can inform a list of files or diretories to be processed or you can process a single file:

```sh
python advisor.py ../texts  # process the entire diretory and subdirectories
python advisor.py ../texts/text1.md  # process a single file
python advisor.py ../texts/dir1 ../texts/text1.md ../texts/text5.md  # will process a single directory and subdirs and two specific files
```

Use `-h` flag for further help.


## License
Distributed under the MIT License. See LICENSE for more information.
