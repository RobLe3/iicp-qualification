# Pinned source references

This is an informative source index for the reviewed supplement, not a qualification authority. Commit links identify exact observed bytes, not continuously current branch state.

## SDK runtime metadata

| Component / source role | Exact source | SHA-256 |
|---|---|---|
| client-python / qualified | [pyproject.toml](https://github.com/RobLe3/iicp-client-python/blob/9c5b3d894ee89ef9fcde52ea0ad99d388ed62183/pyproject.toml) | `a34e7b4e3c852a4bd0cc58516d12d033234e30436a1c34680f11c04ea912067b` |
| client-python / current_public_main | [pyproject.toml](https://github.com/RobLe3/iicp-client-python/blob/6504a6001003cf3a95c16614101da94fe8adcb50/pyproject.toml) | `a34e7b4e3c852a4bd0cc58516d12d033234e30436a1c34680f11c04ea912067b` |
| client-typescript / qualified | [package.json](https://github.com/RobLe3/iicp-client-typescript/blob/97c768d8b9e90756773103e432c273a7d98ba08e/package.json) | `528d2f8ea9e25d3e7efbd8a3f61da837ad8d72951ce0f7bdb2326af0b458228d` |
| client-typescript / current_public_main | [package.json](https://github.com/RobLe3/iicp-client-typescript/blob/65f2c213d321a400f1f92d89ab138519d9b2b11f/package.json) | `528d2f8ea9e25d3e7efbd8a3f61da837ad8d72951ce0f7bdb2326af0b458228d` |

The original candidate archive and member digests appear in `analysis.json`. Those bytes were inspected privately; they are not distributed here. Python specifier term order differs between pyproject metadata and wheel metadata, without changing the observed two-term restriction. This index does not claim registry publication or every runtime patch/interpreter was tested.

## Canonical policy and acceptance

Root source is pinned at `106aae6568d12884603068e82248bf1413371690`. The source repository is access-controlled; a URL is not a promise that every reader can retrieve its contents.

- [Representative policy](https://github.com/RobLe3/iicp.network/blob/106aae6568d12884603068e82248bf1413371690/project/adoption-friction-qualification.json).
- Original finite support scope: `project/pre1-support-matrix.json` in that pinned root.
- Accepted receipt/certificate authority and public verification limits: [current qualification status](../../STATUS.md).
- Owner identifiers and exact body digests are recorded in `analysis.json`; complete private readbacks and source/proof joins remain in the controlled handoff. Live issue state is not immutable acceptance evidence.

## Public versus private verification

Public tests validate the fixed, reviewed derivative, schema, narrative, manifest and non-promotion boundaries. They do not re-read original packages, reconstruct private execution outputs, prove every clause or establish independent interoperability. Private non-authoring review digests are pinned in the derivative; those reviews are not external certification.
