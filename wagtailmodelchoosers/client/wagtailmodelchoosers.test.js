/* eslint-disable */
import ModelChooser, { BaseChooser, ModelPicker, initModelChooser } from './wagtailmodelchoosers';

describe('wagtailmodelchooser', () => {
  it('BaseChooser', () => {
    expect(BaseChooser).toBeDefined();
  });

  it('ModelChooser', () => {
    expect(ModelChooser).toBeDefined();
  });

  it('ModelPicker', () => {
    expect(ModelPicker).toBeDefined();
  });

  describe('initModelChooser', () => {
    it('exists', () => {
      expect(initModelChooser).toBeDefined();
    });
  });
});
