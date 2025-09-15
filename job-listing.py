import sys
import mimetypes
import base64

def get_css(header_hex: str) -> str:
    result = """
        .root {
            --header-backgroud-color: #""" + header_hex + """
        }
    """
    with open(__file__.removesuffix(".py") + ".css") as file:
        return result + file.read()

def get_img_src(path: str) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"

def get_html(job_type: str, company_name: str, logo_path: str, text: str,
                link: str) -> str:
    return f"""
    <div class="card">
        <div class="card-header">{job_type}</div>
        <img class="card-logo" src="{get_img_src(logo_path)}"
            alt="{company_name}">
        <div class="card-content">{text}</div>
        <div class="card-footer">
          <a href="{link}">Les mer</a>
        </div>
    </div>
    """

def getCard(job_type: str, company_name: str, logo_path: str, job_description:
            str, link: str) -> str:
    job_type = job_type.capitalize()
    hex_codes = {
        "Sommerjobb": "ff8abe",
        "Graduate": "8EDFE3",
        "Deltid": "e26aff",
        "Trainee": "62d2e8",
        "Fulltid": "ffbe33"
    }
    if job_type not in hex_codes.keys():
        print(f"Invalid job type: {job_type}. Valid job types:")
        for key in hex_codes.keys():
            print(key)
        return ""

    if len(job_description) > 150:
        print("Too long description")
        return ""

    return f"""
        <style>
            {get_css(hex_codes[job_type])}
        </style>
        {get_html(
            job_type, company_name, logo_path, job_description, link
        )}
    """
    
def help() -> str:
    return (
            f"Usage: python3 {__file__} <job type> <company name>"
            + " <path to logo> <short job description> <link to job listing>"
            )
            
def main(args: list[str]) -> None:
    if (len(args) != 6):
        print(help())
        return

    print(getCard(args[1], args[2], args[3], args[4], args[5]))

if __name__ == "__main__":
    main(sys.argv)
