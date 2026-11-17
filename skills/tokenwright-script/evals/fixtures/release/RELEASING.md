# Releasing (we do this by hand every week)

1. Read the version from VERSION (one line, like 1.4.2).
2. Bump the patch number and write it back to VERSION.
3. Add a heading "## <new version>" at the top of CHANGELOG.md, under the title line.
4. Write the new version into package.json's "version" field.
