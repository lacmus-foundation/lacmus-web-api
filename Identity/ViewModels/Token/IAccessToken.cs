using System.Collections.Generic;

namespace Identity.ViewModels.Token
{
    public interface IAccessToken
    {
        public List<string> Roles { get; set; }
    }
}