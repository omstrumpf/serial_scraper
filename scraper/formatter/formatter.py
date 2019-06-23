from scraper.chapter import Chapter


class Formatter:
    @staticmethod
    def __escape(text):
        return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in text)

    @staticmethod
    def format(chapter: Chapter) -> str:
        return f"""
        <DOCTYPE html>
        <html lang="en">
            <head>
                <title>{chapter.title}</title>
                <meta name="author" content="{chapter.author}"></meta>
            </head>
            <body>
                <h3>{chapter.title}</h3>
                <div align="left">
                {Formatter.__escape(chapter.body)}
                </div>
            </body>
        </html>
        """
