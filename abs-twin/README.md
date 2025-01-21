Contents of this directory

All models replay the traces contained in `../logextractor/trace.db`.

- twin.abs: twin using time delays for trace replaying
- twin-cost.abs: twin using costs for trace replaying (currently
  unconstrainted DCs since we don't have a deployment model)
- twin-cost-2.abs: likewise, but with smaller deployment components
  (currently hard-coded resource constraints in absence of a
  deployment model)
