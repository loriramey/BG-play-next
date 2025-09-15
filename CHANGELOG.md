# Changelog
All notable changes to **Play Next** are documented here.  
This project follows [Semantic Versioning](https://semver.org/).

## [2.0.0] - 2025-Sept
IN PROGRESS

### Added
- Explore page: search by game title and designer, with filters (players, weight, playtime, year, rating).
- Affiliate links (Amazon/eBay) on results for modern titles for easy transfer to online store pages

### Changed
- Fuzzy search overhaul: exact-match priority, multi-edition display `(Year)`, startswith boosting.

### Fixed
- Classic and popular titles (e.g., *Clue*, *Risk*, *Root*) now reliably appear in search.
- Rating display defaults to raw user average to match BGG expectations.

### Deprecated
- TBD

### Removed
- TBD

### Security
- TBD

## [1.0.0] - 2025-Apr
### Added
- Initial base app: cosine-similarity recommendations, fuzzy matching, filters, and data visualizations.
- Two versions exist of this app: 
  - This version is for Streamlit to run
  - There's another repo elsewhere with deeper files and more under-the-hood info about the underlying ML calculations
