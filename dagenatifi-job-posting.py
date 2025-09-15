import sys
import mimetypes
import base64

def get_CSS(header_hex: str) -> str:
    result = """
        .root {
            --header-backgroud-color: #""" + header_hex + """
        }
    """
    with open("style.css") as file:
        return result + file.read()

def get_img_src(path: str) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"

def get_card_html(job_type: str, company_name: str, logo_path: str, text: str,
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

def help() -> str:
    return (
            "Usage: python3 dagenatifi-job-posting.py <job type> <company name>"
            + " <path to logo> <short job description> <link to job listing>"
            )
            
def main(args: list[str]) -> None:
    if (len(args) != 6):
        print(help())
        return

    job_type = args[1].capitalize()
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
        return

    description = args[4]
    if len(description) > 150:
        print("Too long description")
        return

    print(f"""
          <style>
              {get_CSS(hex_codes[job_type])}
          </style>
          {get_card_html(job_type, args[2], args[3], description, args[5])}
          """)

if __name__ == "__main__":
    main(sys.argv)
