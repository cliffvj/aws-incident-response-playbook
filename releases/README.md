# Release History

This directory preserves release notes inside the repository. GitHub Releases publishes the same notes against immutable Git tags and automatically provides source archives.

| Version | Name | Status |
|---|---|---|
| [v2.0.0](v2.0.0.md) | Production Documentation | Current |
| [v1.4.0](v1.4.0.md) | Decision Intelligence | Released |
| [v1.3.0](v1.3.0.md) | Threat and Response Framework Alignment | Released |
| [v1.2.0](v1.2.0.md) | Visual Documentation | Released |
| v1.1.0 | Repository Professionalization | Released; add the historical note here if it was not committed previously. |
| v1.0.0 | Initial Release | Released |

## Publishing workflow

1. Merge the release pull request.
2. Pull the updated `main` branch.
3. Create and push the annotated tag.
4. Create a GitHub Release from the tag.
5. Paste the corresponding Markdown file into the GitHub Release description.
6. Mark only the newest stable version as the latest release.

[Changelog](../CHANGELOG.md) · [Roadmap](../ROADMAP.md)
