# Galactic CMS - Themes

## Theme Prerequisites
In order for Galactic to successfully install a theme, the theme directory must contain these files:

- base.html
- config.json
- CHANGELOG.md
- README.md

## config.json Structure

A theme's config.json file should adhere to the following structure:

```jquery
{
    "theme": {
        "name": "Copernicus",
        "description": "Galactic's default Copernicus theme",
        "author": "Stuart McColl",
        "author-website": "http://www.stuartmccoll.co.uk",
        "config-name": "copernicus"
    }
}
```

The `config-name` value **must** match the name of the theme's directory and must only contain alphanumeric characters and underscores.

## Theme Installation
The Galactic administrator interface allows for simple installation of themes:

- Unzip the theme's directory into the templates/themes directory.
- Ensure that the correct information is contained within the theme's config.json file.
- Log into the Galactic administrator interface.
- Locate the theme on the Dashboard page and then click on the 'Activate' button.