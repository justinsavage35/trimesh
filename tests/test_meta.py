try:
    from . import generic as g
except BaseException:
    import generic as g


class MetaTest(g.unittest.TestCase):

    def test_glb(self):
        # check to see if both `Scene.metadata` and
        # `Scene.geometry._.metadata` is preserved

        # create an example scene
        s = g.trimesh.Scene([
            g.trimesh.creation.box().permutate.transform(),
            g.trimesh.creation.box().permutate.transform(),
            g.trimesh.creation.box().permutate.transform()])

        # add some basic metadata
        s.metadata['hi'] = True
        s.metadata['10'] = "it's true!"
        for m in s.geometry.values():
            # create some random metadata for each mesh
            # note that JSON doesn't support integers as keys
            # so convert integers to strings for comparison
            m.metadata.update(g.np.random.randint(
                0, 1000, 10).reshape((-1, 2)).astype(str))

        # reload the exported scene
        r = g.trimesh.load(file_obj=g.trimesh.util.wrap_as_stream(
            s.export(file_type='glb')),
            file_type='glb')
        # all scene metadata should have survived export-import cycle
        assert r.metadata == s.metadata

        # all geometry should have the same names
        assert set(r.geometry.keys()) == set(s.geometry.keys())

        for k, a in s.geometry.items():
            # `a` is the original mesh
            # `b` is the same mesh after export-import
            b = r.geometry[k]

            # the original metadata should have all survived
            # the exporter is allowed to add additional keys
            assert set(b.metadata.keys()).issuperset(
                a.metadata.keys())

            # every original value must match exactly
            assert all(b.metadata[k] == v for k, v in a.metadata.items())


if __name__ == '__main__':
    g.trimesh.util.attach_to_log()
    g.unittest.main()
